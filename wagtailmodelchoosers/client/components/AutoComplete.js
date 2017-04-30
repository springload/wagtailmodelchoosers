import React, { PropTypes, Component } from 'react';
import Autosuggest from 'react-autosuggest';

const getSuggestionValue = suggestion => suggestion.name;
const renderSuggestion = () => null;

const defaultProps = {
  filter: '',
};

const propTypes = {
  onLoadSuggestions: PropTypes.func.isRequired,
  onLoadStart: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  endpoint: PropTypes.string.isRequired,
  filter: PropTypes.string,
};

class AutoComplete extends Component {
  constructor(props) {
    super(props);

    this.state = {
      value: '',
      suggestions: [],
    };

    this.loadSuggestions = this.loadSuggestions.bind(this);
    this.onSuggestionsUpdateRequested = this.onSuggestionsUpdateRequested.bind(this);
    this.onChange = this.onChange.bind(this);
  }

  loadSuggestions(suggestionValue) {
    const { filter, endpoint, onLoadSuggestions } = this.props;
    const url = `${endpoint}/?search=${suggestionValue}${filter}`;

    fetch(url, {
      credentials: 'same-origin',
    })
      .then(res => res.json())
      .then(json => {
        this.setState({
          suggestions: json.results,
          loading: false,
        }, () => {
          onLoadSuggestions(json.results);
        });
      });
  }

  onSuggestionsUpdateRequested({ value }) {
    const { onLoadStart } = this.props;
    onLoadStart();
    this.loadSuggestions(value);
  }

  onChange(event, { newValue }) {
    const { onChange } = this.props;

    this.setState({
      value: newValue,
    }, () => {
      onChange(newValue);
    });
  }

  render() {
    const { value, suggestions } = this.state;

    return (
      <div>
        <Autosuggest
          suggestions={suggestions}
          onSuggestionsUpdateRequested={this.onSuggestionsUpdateRequested}
          getSuggestionValue={getSuggestionValue}
          renderSuggestion={renderSuggestion}
          inputProps={{
            placeholder: 'Type to search',
            value: value,
            onChange: this.onChange,
          }}
        />
      </div>
    );
  }
}

AutoComplete.defaultProps = defaultProps;
AutoComplete.propTypes = propTypes;

export default AutoComplete;
