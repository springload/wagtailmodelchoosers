import React from "react";
import ReactDOM from "react-dom";

import "./wagtailmodelchoosers.css";

import BaseChooser from "./components/BaseChooser";
import ModelChooser from "./components/ModelChooser";
import ModelPicker from "./components/ModelPicker";
import RemoteModelChooser from "./components/RemoteModelChooser";

const renderWhenReady = (remote, id, data) => {
    const input = document.getElementById(id);

    if ((input as any).value === "loading") {
        setTimeout((() => renderWhenReady(remote, id, data)), 500);
        return;
    }

    const remote_str = remote ? "remote-" : "";
    const control = input.parentNode.querySelector(`[data-${remote_str}model-chooser-mount]`);
    const comp = remote
                 ? <RemoteModelChooser input={input} options={data} />
                 : <ModelChooser input={input} options={data} />
    ReactDOM.render(comp, control);
};

const initModelChooser = (id: string, data: any) => {
    console.log("initModelChooser id: ", id);
    console.log("initModelChooser data: ", data);

    const input = document.getElementById(id);

    if (input) {
        renderWhenReady(false, id, data)
    }
};

const initRemoteModelChooser = (id: string, data: any) => {
    console.log("initRemoteModelChooser id: ", id);
    console.log("initRemoteModelChooser data: ", data);

    const input = document.getElementById(id);

    if (input) {
        renderWhenReady(true, id, data)
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
