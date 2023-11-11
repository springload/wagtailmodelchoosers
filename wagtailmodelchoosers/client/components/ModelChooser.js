import PropTypes from 'prop-types';
import React from 'react';
import BaseChooser from './BaseChooser';

class ModelChooser extends React.Component {
  constructor(props) {
    super(props);


    this.updateInputValue = this.updateInputValue.bind(this);

    if (!parseInt(props.input.value)) {
        this.state = {initialValue: null};
        return;
    }

    this.state = {initialValue: -1};

    const url = props.options.endpoint + "?id=" + props.input.value;
    fetch(url, { credentials: 'same-origin' })
    .then(res => res.json())
    .then((json) => {
      this.setState({initialValue: json.results[0]});
    });
  }

  updateInputValue(item) {
    const { input, options: { pk_name } } = this.props;
    let newValue;

    if (item === null) {
      // Null state
      newValue = null;
    } else {
      const id = item[pk_name];

      if (typeof id === 'string') {
        // Strings (Eg UUID)
        newValue = id.replace(/ /g, '');
      } else {
        // Numbers
        newValue = id;
      }
    }

    // TODO: Props mutation WTF?
    input.value = newValue;
  }

  render() {
    if (this.state.initialValue === -1) return "";

    return (
      <BaseChooser
        initialValue={this.state.initialValue}
        updateInputValue={this.updateInputValue}
        {...this.props.options}
      />
    );
  }
}

ModelChooser.propTypes = {
  // eslint-disable-next-line react/forbid-prop-types
  options: PropTypes.object.isRequired,
  // eslint-disable-next-line react/forbid-prop-types
  input: PropTypes.object.isRequired,
};

export default ModelChooser;
