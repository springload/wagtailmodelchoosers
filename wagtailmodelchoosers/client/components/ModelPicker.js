import PropTypes from 'prop-types';
import React from 'react';
import Button, { CloseButton } from './Buttons';
import AutoComplete from './AutoComplete';
import { pluralize, tr } from '../utils';

const MODAL_EXIT_CLASS = 'admin-modal--exit';
const MODAL_CLOSE_TIMEOUT = 400;
const MODAL_OPEN_TIMEOUT = 650;

const STR = {
  choose: 'Choose',
  result: 'Result',
  results: 'Results',
  previous: 'Previous',
  page: 'Page',
  pages: 'Pages',
  next: 'Next',
};

const defaultProps = {
  filters: [],
  page_size: 10,
  page_size_param: 'page_size',
  translations: {},
};

const propTypes = {
  onSelect: PropTypes.func.isRequired,
  onClose: PropTypes.func.isRequired,
  label: PropTypes.string.isRequired,
  endpoint: PropTypes.string.isRequired,
  list_display: PropTypes.array.isRequired,
  filters: PropTypes.array,
  pk_name: PropTypes.string.isRequired,
  page_size: PropTypes.number,
  page_size_param: PropTypes.string,
  translations: PropTypes.object,
};

class ModelPicker extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      pickerVisible: false,
      models: [],
      loading: true,
      next: false,
      previous: false,
      count: 0,
      url: null,
      numPages: 0,
      page: 0,
      suggestions: [],
      suggestionsCount: 0,
      shouldShowSuggestions: false,
      loadingSuggestions: false,
    };

    this.getDefaultUrl = this.getDefaultUrl.bind(this);
    this.getPk = this.getPk.bind(this);
    this.getModels = this.getModels.bind(this);
    this.select = this.select.bind(this);
    this.closeWithCallback = this.closeWithCallback.bind(this);
    this.update = this.update.bind(this);
    this.addFilterParams = this.addFilterParams.bind(this);
    this.navigate = this.navigate.bind(this);
    this.onClose = this.onClose.bind(this);
    this.handleError = this.handleError.bind(this);
    this.getPlaceholder = this.getPlaceholder.bind(this);
    this.getTable = this.getTable.bind(this);
    this.getHeader = this.getHeader.bind(this);
    this.parseValue = this.parseValue.bind(this);
    this.getRow = this.getRow.bind(this);
    this.getCount = this.getCount.bind(this);
    this.getCountDisplay = this.getCountDisplay.bind(this);
    this.getPageDisplay = this.getPageDisplay.bind(this);
    this.getPaginationButtons = this.getPaginationButtons.bind(this);
    this.navigatePrevious = this.navigatePrevious.bind(this);
    this.navigateNext = this.navigateNext.bind(this);
    this.onLoadSuggestions = this.onLoadSuggestions.bind(this);
    this.onValueChange = this.onValueChange.bind(this);
    this.onLoadStart = this.onLoadStart.bind(this);
  }

  componentDidMount() {
    setTimeout(() => {
      this.navigate(this.getDefaultUrl());
    }, MODAL_OPEN_TIMEOUT);

    document.body.style.overflow = 'hidden';
    document.body.style.width = `${document.body.offsetWidth}px`;
  }

  componentWillUnmount() {
    document.body.style.overflow = '';
    document.body.style.width = '';
  }

  onClose(e) {
    const { onClose } = this.props;
    this.closeWithCallback(() => {
      onClose(e);
    });
  }

  onLoadSuggestions(suggestions) {
    this.setState({
      suggestions,
      suggestionsCount: suggestions.length,
      loadingSuggestions: false,
    });
  }

  onValueChange(newValue) {
    const shouldShowSuggestions = newValue.trim().length > 2;

    this.setState({
      shouldShowSuggestions,
    });
  }

  onLoadStart() {
    this.setState({
      loadingSuggestions: true,
    });
  }

  getPaginationButtons() {
    const { translations } = this.props;
    const { next, previous, shouldShowSuggestions } = this.state;

    const prevLabel = tr(STR, translations, 'previous');
    const nextLabel = tr(STR, translations, 'next');
    const prevEnabled = shouldShowSuggestions ? false : !!previous;
    const nextEnabled = shouldShowSuggestions ? false : !!next;

    return (
      <span>
        <Button
          onClick={this.navigatePrevious}
          isActive={prevEnabled}
          label={prevLabel}
        />
        <Button
          onClick={this.navigateNext}
          isActive={nextEnabled}
          label={nextLabel}
        />
      </span>
    );
  }

  getPageDisplay() {
    const { translations } = this.props;
    const { numPages, page: currentPage, shouldShowSuggestions } = this.state;

    let text;
    if (shouldShowSuggestions) {
      const label = tr(STR, translations, 'page');
      text = `1 / 1 ${label}`;
    } else {
      const label = pluralize(STR, translations, 'result', 'results', numPages);
      text = `${currentPage} / ${numPages} ${label}`;
    }

    return <span className="admin-modal__pagination">{text}</span>;
  }

  getCountDisplay() {
    const { translations } = this.props;
    const count = this.getCount();
    const label = pluralize(STR, translations, 'result', 'results', count);

    return (
      <span className="admin-modal__results">
        {count} {label}
      </span>
    );
  }

  getRow(item) {
    const { list_display: listDisplay } = this.props;

    return ( // eslint-disable-next-line
      <tr
        key={this.getPk(item)}
        className="chooser__item"
        onClick={() => this.select(this.getPk(item))}
      >
        {listDisplay.map((field) => {
          const value = item[field.name];

          return (
            <td key={field.name} className="chooser__cell">
              {this.parseValue(value, field.name)}
            </td>
          );
        })}
      </tr>
    );
  }

  getCount() {
    const { count, shouldShowSuggestions, suggestionsCount } = this.state;

    return shouldShowSuggestions ? suggestionsCount : count;
  }

  // eslint-disable-next-line
  getHeader(field) {
    return (
      <td key={field.name}>
        {field.label}
      </td>
    );
  }

  getTable() {
    const { list_display: listDisplay } = this.props;
    const models = this.getModels();

    return (
      <table className="chooser-table">
        <thead>
          <tr>
            {listDisplay.map(this.getHeader)}
          </tr>
        </thead>
        <tbody>
          {models.length ? models.map(this.getRow) : this.getPlaceholder()}
        </tbody>
      </table>
    );
  }

  getPlaceholder() {
    const { list_display: listDisplay } = this.props;
    const { loading } = this.state;

    return (
      <tr className="chooser__item">
        <td colSpan={listDisplay.length} className="chooser__cell chooser__cell--disabled">
          {loading ? 'Loading' : 'Sorry, no results'}
        </td>
      </tr>
    );
  }

  getModels() {
    const { shouldShowSuggestions, suggestions, models } = this.state;

    return shouldShowSuggestions ? suggestions : models;
  }

  getPk(item) {
    const { pk_name } = this.props;

    return item ? item[pk_name] : null;
  }

  getDefaultUrl() {
    const { endpoint, page_size: pageSize, page_size_param: pageSizeParam } = this.props;
    return `${endpoint}/?${pageSizeParam}=${pageSize}`;
  }

  select(pk) {
    const { onSelect } = this.props;
    const { url } = this.state;
    const models = this.getModels();
    const item = models.find(m => this.getPk(m) === pk);

    this.closeWithCallback(() => {
      onSelect(this.getPk(item), item, url);
    });
  }

  navigateNext() {
    const { shouldShowSuggestions, page } = this.state;

    if (shouldShowSuggestions) {
      return;
    }

    const url = `${this.getDefaultUrl()}&page=${page + 1}`;
    this.navigate(url);
  }

  navigatePrevious() {
    const { shouldShowSuggestions, page } = this.state;

    if (shouldShowSuggestions) {
      return;
    }

    const url = `${this.getDefaultUrl()}&page=${page - 1}`;
    this.navigate(url);
  }

  // eslint-disable-next-line
  parseValue(value, fieldName) {
    const type = typeof value;

    if (type === 'string') {
      return value;
    }

    if (type === 'number') {
      return value;
    }

    if (type === 'object') {
      // Django internals
      if (fieldName === 'content_type') {
        return value.model;
      }
    }

    if (type === 'boolean') {
      return value ? 'True' : 'False';
    }

    return '';
  }

  handleError() {
    this.setState({
      loading: false,
    });
  }

  navigate(url) {
    const urlWithFilters = this.addFilterParams(url);
    this.setState({
      loading: true,
      url,
    }, () => {
      // TODO There is no reason for this code to be in the setState callback.
      // TODO This is not producing errors when status code is not 200,
      // so the error handling likely does not work.
      // TODO Use fetch API wrapper.
      fetch(urlWithFilters, {
        credentials: 'same-origin',
      })
        .then(res => res.json())
        .then(this.update, this.handleError);
    });
  }

  addFilterParams(url) {
    const { filters } = this.props;
    let localUrl = url;

    if (filters) {
      // TODO Redo with map and join.
      filters.forEach((filter) => {
        localUrl += `&${filter.field}=${filter.value}`;
      });
    }

    return localUrl;
  }

  update(json) {
    const { page_size: pageSize } = this.props;

    // If the API does not return the total number of page,
    // try to calculate it from the number of result and the page size.
    let numPage = 0;
    if (json.num_pages) {
      numPage = json.num_pages;
    } else if (json.count) {
      numPage = Math.ceil(json.count / pageSize);
    }

    this.setState({
      numPages: numPage,
      page: json.page,
      models: json.results,
      count: json.count,
      next: json.next,
      previous: json.previous,
      loading: false,
    }, () => {
      this.contentRef.scrollTop = 0;
    });
  }

  closeWithCallback(callback) {
    this.elRef.classList.add(MODAL_EXIT_CLASS);
    setTimeout(callback, MODAL_CLOSE_TIMEOUT);
  }

  render() {
    const { endpoint, label, translations } = this.props;
    const chooseHeading = tr(STR, translations, 'choose');

    return (
      <div className="modal admin-modal" ref={(el) => { this.elRef = el; }}>
        <div className="admin-modal__dialog">
          <div className="admin-modal__header">
            <h2>{chooseHeading} {label}</h2>
            <CloseButton onClick={this.onClose} />
          </div>
          <div className="admin-modal__actions">
            <div className="admin-modal__action">
              <AutoComplete
                onChange={this.onValueChange}
                onLoadSuggestions={this.onLoadSuggestions}
                onLoadStart={this.onLoadStart}
                endpoint={endpoint}
                filter={this.addFilterParams('')}
              />
            </div>
            <div className="admin-modal__action">
              {this.getCountDisplay()}
              {this.getPageDisplay()}
              {this.getPaginationButtons()}
            </div>
          </div>
          <div className="admin-modal__content" ref={(content) => { this.contentRef = content; }}>
            {this.getTable()}
          </div>
        </div>
      </div>
    );
  }
}

ModelPicker.defaultProps = defaultProps;
ModelPicker.propTypes = propTypes;

export default ModelPicker;
