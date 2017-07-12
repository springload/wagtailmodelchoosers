import PropTypes from 'prop-types';
import React from 'react';
import BaseChooser from './BaseChooser';

class RemoteModelChooser extends React.Component {
  constructor(props) {
    super(props);

    this.updateInputValue = this.updateInputValue.bind(this);
  }

  updateInputValue(item) {
    const { input, options: { fields_to_save: fieldsToSave } } = this.props;
    let newValue;

    if (item === null) {
      // Null state
      newValue = null;
    } else if (fieldsToSave) {
      // Create a new object with only the fields to save
      const clone = {};
      fieldsToSave.forEach((field) => {
        clone[field] = item[field];
      });
      newValue = JSON.stringify(clone);
    } else {
      // Use the whole object.
      newValue = JSON.stringify(item);
    }

    // TODO: Props mutation WTF?
    input.value = newValue;
  }

  render() {
    const { input, options } = this.props;
    let initialValue;
    try {
      // TODO: Should we use safe-parse or something alike?
      initialValue = JSON.parse(input.value);
    } catch (err) {
      initialValue = {};
    }

    return (
      <BaseChooser
        initialValue={initialValue}
        updateInputValue={this.updateInputValue}
        {...options}
      />
    );
  }
}

RemoteModelChooser.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  options: PropTypes.object.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  input: PropTypes.object.isRequired,
};

export default RemoteModelChooser;
