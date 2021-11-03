import { ContentState } from "draft-js";
import React from "react";

type Props = {
    entityKey?: string;
    contentState: ContentState;
    children?: React.ReactNode;
};

const DefaultDecorator = (entityData: any, props: Props) => {
    console.log("DefaultDecorator entityData: ", entityData);
    console.log("DefaultDecorator props: ", props);

    const { entityKey, contentState, children } = props;
    const d = contentState.getEntity(entityKey).getData();
    const { id } = d;

    const prefixLabel = entityData.prefix_label || "";
    const prefix = `#${id} ${prefixLabel} - `;

    return (
        <span data-tooltip={entityKey} className="RichEditor-link">
            {prefix}
            {children}
        </span>
    );
};

export default DefaultDecorator;
