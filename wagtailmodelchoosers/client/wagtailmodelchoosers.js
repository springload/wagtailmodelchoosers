import React from 'react';
import ReactDOM from 'react-dom';

import './wagtailmodelchoosers.css';

import BaseChooser from './components/BaseChooser';
import ModelChooser from './components/ModelChooser';
import ModelPicker from './components/ModelPicker';
import RemoteModelChooser from './components/RemoteModelChooser';
import ModelSource from './sources/ModelSource';
import RemoteModelSource from './sources/RemoteModelSource';
import GenericModelDecorator from './decorators/GenericModelDecorator';

const initModelChooser = (id, data) => {
  const input = document.getElementById(id);

  if (input) {
    const item = input.parentNode;
    const control = item.querySelector('[data-model-chooser-mount]');
    ReactDOM.render(<ModelChooser input={input} options={data} />, control);
  }
};

const initRemoteModelChooser = (id, data) => {
  const input = document.getElementById(id);

  if (input) {
    const item = input.parentNode;
    const control = item.querySelector('[data-remote-model-chooser-mount]');
    ReactDOM.render(<RemoteModelChooser input={input} options={data} />, control);
  }
};

window.wagtailModelChoosers = {};
window.wagtailModelChoosers.initModelChooser = initModelChooser;
window.wagtailModelChoosers.initRemoteModelChooser = initRemoteModelChooser;
window.wagtailModelChoosers.ModelSource = ModelSource;
window.wagtailModelChoosers.RemoteModelSource = RemoteModelSource;
window.wagtailModelChoosers.GenericModelDecorator = GenericModelDecorator;

// Add Sources to WagtailDraftail if available.
// This is for backward compatibility for projects still using WagtailDraftail
// despite upgrading Wagtail 2.0 which has Draftail built-in.
if (Object.prototype.hasOwnProperty.call(window, 'wagtailDraftail')) {
  window.wagtailDraftail.registerSources({ ModelSource, RemoteModelSource });
}

export default ModelChooser;

export {
    BaseChooser,
    ModelPicker,
    RemoteModelChooser,
    initModelChooser,
    initRemoteModelChooser,
};
