import PropTypes from 'prop-types';
import React from 'react';
import { Modifier, EditorState } from 'draft-js';
import ModelPicker from '../components/ModelPicker';

const API_BASE_URL = '/admin/modelchoosers/api/v1';


class ModelSource extends React.Component {
  constructor(props) {
    super(props);
    this.onSelected = this.onSelected.bind(this);
  }

  onSelected(id, data) {
    const {
      editorState,
      onComplete,
      entityType: {
        content_type,
        display = 'title',
        pk_name: pkName = 'uuid',
        type,
        icon,
        icon_name,
        fields_to_save: fieldsToSave = [],
      }
    } = this.props;

    let label;
    const displayIsSelection = display === '__selection__';

    const currentContent = editorState.getCurrentContent();
    const selectionState = editorState.getSelection();

    if (displayIsSelection) {
      // If display is selection, get label for the new entity from selected text
      // TODO: What if no text is selected?
      const anchorKey = selectionState.getAnchorKey();
      const currentContentBlock = currentContent.getBlockForKey(anchorKey);

      const start = selectionState.getStartOffset();
      const end = selectionState.getEndOffset();

      label = currentContentBlock.getText().slice(start, end);
    } else {
      // Otherwise, assume 'display' is an array of fields to lookup in the selected
      // data for a label name.  If none match, use pkName as a backup.
      const display_arr = Array.isArray(display) ? display : [display];
      const field = display_arr.find((f) => f in data && data[f]) || pkName;
      label = data[field];
    }

    const fields = Object.fromEntries(fieldsToSave.map((f) => [f, data[f]]));

    // For some reason we have to only store content_type for local models.
    // I have no idea why, just preserving existing functionality.
    const maybeContentType = fieldsToSave.length === 0 ? {content_type} : {};

    const nextData = {
      id,
      label,
      ...fields,
      ...maybeContentType,
    };

    const entityMutability = displayIsSelection ? 'MUTABLE' : 'IMMUTABLE';
    const entity = currentContent.createEntity(type, entityMutability, nextData);
    const entityKey = entity.getLastCreatedEntityKey();

    const newContent = Modifier.replaceText(currentContent, selectionState, label, null, entityKey);
    const nextState = EditorState.push(editorState, newContent, 'insert-characters');

    onComplete(nextState);
  }

  render() {
    const { entity, entityType } = this.props;
    const { fields_to_save = null } = entityType;
    const model_path = fields_to_save ? 'remote_model' : 'model'
    const endpoint = `${API_BASE_URL}/${model_path}/${entityType.content_type}`;

    return (
      <ModelPicker
        onChange={this.onSelected}
        onSelect={this.onSelected}
        onClose={this.props.onClose}
        entity={entity}
        endpoint={endpoint}
        value={null}
        required={false}
        {...entityType}
      />
    );
  }
}

ModelSource.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  editorState: PropTypes.object.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  options: PropTypes.object.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  entity: PropTypes.object,
  onClose: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
};

ModelSource.defaultProps = {
  entity: {},
};

export default ModelSource;
