import ModelSource from "./sources/ModelSource";
import DefaultDecorator from "./DefaultDecorator";

const WrapDecorator =
    (entityData, decorator) =>
    (...args) =>
        decorator(entityData, ...args);

type Props = {
    modelChooserEntityTypes: any[];
    draftailOptions: any;
    widgetAttrIds: any;
};

const modelChooserDraftailInit = ({
    modelChooserEntityTypes,
    draftailOptions,
    widgetAttrIds,
}: Props) => {
    // Save entities for decorators to use.  Doing this because I can't find a way to get entity type
    // data from within a decorator without saving it to contentstate, which ends up getting saved
    // to DB, which is unnecessary and breaks historical data.

    // Typescript doesn't know about .fromEntries, but it has been polyfilled for IE.
    // @ts-ignore
    const modelChooserDraftailEntities = Object.fromEntries(
        draftailOptions.entityTypes
            .filter((et) => modelChooserEntityTypes.includes(et.type))
            .map((et) => [et.type, et])
    );

    // Register all modelchooser entity plugins.
    modelChooserEntityTypes.forEach((entityType) => {
        const decorators = (window as any).draftailDecorators || {};
        const decorator = decorators[entityType] || DefaultDecorator;
        const plugin = {
            type: entityType,
            source: ModelSource,
            decorator: WrapDecorator(
                modelChooserDraftailEntities[entityType],
                decorator
            ),
        };
        (window as any).draftail.registerPlugin(plugin);
    });

    (window as any).draftail.initEditor(
        widgetAttrIds,
        draftailOptions,
        document.currentScript
    );
};

(window as any).modelChooserDraftailInit = modelChooserDraftailInit;
