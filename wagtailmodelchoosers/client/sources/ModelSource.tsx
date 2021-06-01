import React from "react";
import "../polyfills";
import { Modifier, EditorState } from "draft-js";
import ModelPicker from "../components/ModelPicker";

const API_BASE_URL = "/admin/modelchoosers/api/v1";

type Props = {
    editorState: any;
    options: any;
    entity?: any;
    onClose: () => void;
    onUpdate: () => void;
    onComplete: (nextState: any) => void;
    entityType: any;
};
type State = {};

class ModelSource extends React.Component<Props, State> {
    constructor(props: Props) {
        console.log("ModelSource constructor props: ", props);

        super(props);
        this.onSelected = this.onSelected.bind(this);
    }

    onSelected(id: string, data: any) {
        console.log("onSelected id: ", id);
        console.log("onSelected data: ", data);

        const {
            editorState,
            onComplete,
            entityType: {
                content_type,
                display = "title",
                pk_name: pkName = "uuid",
                type,
                fields_to_save: fieldsToSave = [],
            },
        } = this.props as Props;

        let label: string;
        const displayIsSelection = display === "__selection__";

        const currentContent = editorState.getCurrentContent();
        const selectionState = editorState.getSelection();

        if (displayIsSelection) {
            // If display is selection, get label for the new entity from selected text
            // TODO: What if no text is selected?
            const anchorKey = selectionState.getAnchorKey();
            const currentContentBlock =
                currentContent.getBlockForKey(anchorKey);

            const start = selectionState.getStartOffset();
            const end = selectionState.getEndOffset();

            label = currentContentBlock.getText().slice(start, end);
        } else {
            // Otherwise, assume 'display' is an array of fields to lookup in the selected
            // data for a label name.  If none match, use pkName as a backup.
            const display_arr = Array.isArray(display) ? display : [display];
            const field =
                display_arr.find((f) => f in data && data[f]) || pkName;
            label = data[field];
        }

        // Typescript doesn't know about .fromEntries, but it has been polyfilled for IE.
        // @ts-ignore
        const fields = Object.fromEntries(
            fieldsToSave.map((f) => [f, data[f]])
        );

        // For some reason we have to only store content_type for local models.
        // I have no idea why, just preserving existing functionality.
        const maybeContentType =
            fieldsToSave.length === 0 ? { content_type } : {};

        const nextData = {
            id,
            label,
            ...fields,
            ...maybeContentType,
        };

        const entityMutability = displayIsSelection ? "MUTABLE" : "IMMUTABLE";
        const entity = currentContent.createEntity(
            type,
            entityMutability,
            nextData
        );
        const entityKey = entity.getLastCreatedEntityKey();

        const newContent = Modifier.replaceText(
            currentContent,
            selectionState,
            label,
            null,
            entityKey
        );
        const nextState = EditorState.push(
            editorState,
            newContent,
            "insert-characters"
        );

        onComplete(nextState);
    }

    render() {
        const { entity, entityType } = this.props as Props;
        const { remote_endpoint = null } = entityType;
        const model_path = remote_endpoint ? "remote_model" : "model";
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

export default ModelSource;
