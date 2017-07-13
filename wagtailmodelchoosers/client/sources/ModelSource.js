import PropTypes from 'prop-types';
import React from 'react';
import { DraftUtils } from 'draftail';

import ModelPicker from '../components/ModelPicker';

const API_BASE_URL = '/admin/modelchoosers/api/v1/model/';

class ModelSource extends React.Component {
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
    const { editorState, onUpdate, options: { content_type, display = 'title', pk_name: pkName = 'uuid', type } } = this.props;
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
        for (const fieldName of display) {
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
    const nextData = {
      id: id,
      label: label,
      content_type: content_type,
    };

    const nextState = DraftUtils.createEntity(
      editorState,
      type,
      nextData,
      nextData.label,
      entityMutability
    );

    onUpdate(nextState);
  }

  render() {
    const { entity, options } = this.props;
    const endpoint = `${API_BASE_URL}${options.content_type}`;

    return (
      <ModelPicker
        onChange={this.onSelected}
        onSelect={this.onSelected}
        onClose={this.onClose}
        entity={entity}
        endpoint={endpoint}
        value={null}
        required={false}
        {...options}
      />
    );
  }
}

ModelSource.propTypes = {
  editorState: PropTypes.object.isRequired,
  options: PropTypes.object.isRequired,
  entity: PropTypes.object,
  onClose: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
};

export default ModelSource;
