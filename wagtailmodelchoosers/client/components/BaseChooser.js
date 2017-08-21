import PropTypes from 'prop-types';
import React from 'react';
import { SecondaryButton } from './Buttons';
import ModelPicker from './ModelPicker';
import { tr } from '../utils';

const STR = {
  choose: 'Choose',
  choose_again: 'Choose another',
  clear: 'Clear choice',
};

const defaultProps = {
  display: 'title',
  filters: [],
  translations: {},
  pk_name: 'uuid',
  page_size: 10,
  page_size_param: 'page_size',
};

const propTypes = {
  initialValue: PropTypes.oneOfType([PropTypes.string, PropTypes.object]).isRequired,
  updateInputValue: PropTypes.func.isRequired,
  initial_display_value: PropTypes.string.isRequired,
  required: PropTypes.bool.isRequired,
  display: PropTypes.oneOfType([PropTypes.string, PropTypes.array]).isRequired,
  pk_name: PropTypes.string,
  translations: PropTypes.object,
  label: PropTypes.string.isRequired,
  list_display: PropTypes.array.isRequired,
  filters: PropTypes.array,
  endpoint: PropTypes.string.isRequired,
  page_size: PropTypes.number,
  page_size_param: PropTypes.string,
};

class BaseChooser extends React.Component {

  constructor(props) {
    super(props);

    const { display, initialValue, initial_display_value: initialDisplayValue } = this.props;

    // If `initialValue` is an object (i.e. the item), use it directly,
    // otherwise create a new object and use the `initialValue` for the ID.
    const hasInitialObject = initialValue !== null && typeof initialValue === 'object';
    const selectedItem = hasInitialObject ? initialValue : {};
    const selectedId = hasInitialObject ? this.getItemPk(selectedItem) : initialValue;

    // Ensure the item has the required key for `display`.
    const displayKey = Array.isArray(display) ? display[0] : display;
    if (!(displayKey in selectedItem)) {
      selectedItem[displayKey] = initialDisplayValue;
    }

    this.state = {
      pickerVisible: false,
      selectedId,
      selectedItem,
      initialUrl: null,
    };

    this.showPicker = this.showPicker.bind(this);
    this.onClose = this.onClose.bind(this);
    this.onSelect = this.onSelect.bind(this);
    this.getItemPk = this.getItemPk.bind(this);
    this.getItemPreview = this.getItemPreview.bind(this);
    this.isOptional = this.isOptional.bind(this);
    this.getChooseButtons = this.getChooseButtons.bind(this);
    this.clearPicker = this.clearPicker.bind(this);
  }

  onClose() {
    this.setState({
      pickerVisible: false,
    });
  }

  onSelect(id, item, url) {
    this.setState({
      selectedId: id,
      selectedItem: item,
      pickerVisible: false,
      initialUrl: url,
    }, () => {
      this.props.updateInputValue(item);
    });
  }

  getItemPk(item) {
    const { pk_name: pkName } = this.props;

    return item ? item[pkName] : null;
  }

  getItemPreview() {
    const { display } = this.props;
    const { selectedItem } = this.state;

    if (!selectedItem) {
      return '';
    }

    // Return first non-empty field if `display` is an Array.
    if (Array.isArray(display)) {
      let i;
      for (i = 0; i < display.length; i += 1) {
        const fieldName = display[i];
        if (fieldName in selectedItem && selectedItem[fieldName]) {
          return selectedItem[fieldName];
        }
      }
    }

    // Return the `display` field if available.
    if (display in selectedItem && selectedItem[display]) {
      return selectedItem[display];
    }

    // Return the object PK as default.
    return this.getItemPk(selectedItem);
  }

  getChooseButtons() {
    const { translations } = this.props;
    const { selectedId } = this.state;

    if (!selectedId) {
      return (
        <SecondaryButton
          onClick={this.showPicker}
          label={tr(STR, translations, 'choose')}
        />
      );
    }

    return (
      <span>
        <SecondaryButton
          onClick={this.showPicker}
          label={tr(STR, translations, 'choose_again')}
        />
        {this.isOptional() ? (
          <SecondaryButton
            onClick={this.clearPicker}
            label={tr(STR, translations, 'clear')}
          />
        ) : null}
      </span>
    );
  }

  isOptional() {
    const { required } = this.props;
    return !required;
  }

  showPicker() {
    this.setState({
      pickerVisible: true,
    });
  }

  clearPicker(e) {
    e.preventDefault();

    this.setState({
      selectedId: null,
      selectedItem: null,
      pickerVisible: false,
      initialUrl: null,
    }, () => {
      this.props.updateInputValue(null);
    });
  }

  render() {
    const { pickerVisible, initialUrl } = this.state;
    const {
      list_display: listDisplay,
      label,
      endpoint,
      filters,
      pk_name: pkName,
      page_size: pageSize,
      page_size_param: pageSizeParam,
      translations,
    } = this.props;

    return (
      <div>
        <div>
          <span className="model-chooser__label">
            {this.getItemPreview()}
          </span>
          {this.getChooseButtons()}
        </div>
        {pickerVisible ? (
          <ModelPicker
            url={initialUrl}
            onClose={this.onClose}
            onSelect={this.onSelect}
            label={label}
            endpoint={endpoint}
            filters={filters}
            list_display={listDisplay}
            pk_name={pkName}
            page_size={pageSize}
            page_size_param={pageSizeParam}
            translations={translations}
          />
        ) : null}
      </div>
    );
  }
}

BaseChooser.defaultProps = defaultProps;
BaseChooser.propTypes = propTypes;

export default BaseChooser;
