import React from "react";
import ReactDOM from "react-dom";

import "./wagtailmodelchoosers.css";

import BaseChooser from "./components/BaseChooser";
import ModelChooser from "./components/ModelChooser";
import ModelPicker from "./components/ModelPicker";
import RemoteModelChooser from "./components/RemoteModelChooser";

const initModelChooser = (id: string, data: any) => {
    console.log("initModelChooser id: ", id);
    console.log("initModelChooser data: ", data);

    const input = document.getElementById(id);

    if (input) {
        const item = input.parentNode;
        const control = item.querySelector("[data-model-chooser-mount]");
        ReactDOM.render(<ModelChooser input={input} options={data} />, control);
    }
};

const initRemoteModelChooser = (id: string, data: any) => {
    console.log("initRemoteModelChooser id: ", id);
    console.log("initRemoteModelChooser data: ", data);

    const input = document.getElementById(id);

    if (input) {
        const item = input.parentNode;
        const control = item.querySelector("[data-remote-model-chooser-mount]");
        ReactDOM.render(
            <RemoteModelChooser input={input} options={data} />,
            control
        );
    }
};

(window as any).wagtailModelChoosers = {};
(window as any).wagtailModelChoosers.initModelChooser = initModelChooser;
(window as any).wagtailModelChoosers.initRemoteModelChooser =
    initRemoteModelChooser;

export default ModelChooser;

export {
    BaseChooser,
    ModelPicker,
    RemoteModelChooser,
    initModelChooser,
    initRemoteModelChooser,
};
