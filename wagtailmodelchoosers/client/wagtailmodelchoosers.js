import React from 'react';
import ReactDOM from 'react-dom';

import './wagtailmodelchoosers.css';

import BaseChooser from './components/BaseChooser';
import ModelChooser from './components/ModelChooser';
import ModelPicker from './components/ModelPicker';
import RemoteModelChooser from './components/RemoteModelChooser';

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

export default ModelChooser;

export {
    BaseChooser,
    ModelPicker,
    RemoteModelChooser,
    initModelChooser,
    initRemoteModelChooser,
};
