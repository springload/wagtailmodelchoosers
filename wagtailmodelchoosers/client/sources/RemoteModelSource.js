import PropTypes from 'prop-types';
import React from 'react';
import { AtomicBlockUtils } from 'draft-js';

import ModelPicker from '../components/ModelPicker';

const API_BASE_URL = '/admin/modelchoosers/api/v1/remote_model/';

class RemoteModelSource extends React.Component {
  constructor(props) {
    super(props);
    this.onClose = this.onClose.bind(this);
    this.onSelected = this.onSelected.bind(this);
  }

  onClose() {
    const { onClose } = this.props;
    onClose();
  }

  onSelected(id, data) {
    const { editorState, onComplete, entityType: {
      display = 'title', fields_to_save: fieldsToSave, pk_name: pkName = 'uuid', type } } = this.props;
    let label;
    let entityMutability;
    if (display === '__selection__') {
      const selectionState = editorState.getSelection();
      const anchorKey = selectionState.getAnchorKey();
      const currentContent = editorState.getCurrentContent();
      const currentContentBlock = currentContent.getBlockForKey(anchorKey);
      const start = selectionState.getStartOffset();
      const end = selectionState.getEndOffset();

      label = currentContentBlock.getText().slice(start, end);
      entityMutability = 'MUTABLE';
    } else {
      if (Array.isArray(display)) {
        let i;
        for (i = 0; i < display.length; i + 1) {
          const fieldName = display[i];
          if (fieldName in data && data[fieldName]) {
            label = data[fieldName];
            break;
          }
        }
      } else if (display in data && data[display]) {
        label = data[display];
      }

      if (label === undefined) {
        label = data[pkName];
      }
      entityMutability = 'IMMUTABLE';
    }

    let itemData;
    if (fieldsToSave) {
      // Create a new object with only the fields to save
      const clone = {};
      fieldsToSave.forEach((field) => {
        clone[field] = data[field];
      });
      itemData = clone;
    } else {
      // Use the whole object.
      itemData = data;
    }

    const entityData = Object.assign({}, itemData, {
      id,
      label,
    });

    const contentState = editorState.getCurrentContent();
    const contentStateWithEntity = contentState.createEntity(
      type,
      entityMutability,
      entityData,
    );
    const nextState = AtomicBlockUtils.insertAtomicBlock(
      editorState,
      contentStateWithEntity.getLastCreatedEntityKey(),
      ' ',
    );

    onComplete(nextState);
  }

  render() {
    const { entityType: options } = this.props;
    const endpoint = `${API_BASE_URL}${options.content_type}`;

    return (
      <ModelPicker
        onSelect={this.onSelected}
        onClose={this.onClose}
        endpoint={endpoint}
        value={null}
        required={false}
        {...options}
      />
    );
  }
}

RemoteModelSource.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  editorState: PropTypes.object.isRequired,
  onClose: PropTypes.func.isRequired,
  onComplete: PropTypes.func.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  entityType: PropTypes.object.isRequired,
};

export default RemoteModelSource;
