import ModelSource from './sources/ModelSource';
import DefaultDecorator from './DefaultDecorator';

const WrapDecorator = (entityData, decorator) => (...args) => decorator(entityData, ...args);

const modelChooserDraftailInit = (modelChooserEntityTypes, draftailOptions, widgetAttrIds) => {
  // Save entities for decorators to use.  Doing this because I can't find a way to get entity type
  // data from within a decorator without saving it to contentstate, which ends up getting saved
  // to DB, which is unnecessary and breaks historical data.
  const modelChooserDraftailEntities = Object.fromEntries(
    draftailOptions.entityTypes
      .filter(et => modelChooserEntityTypes.includes(et.type))
      .map(et => [et.type, et]),
  );

  // Register all modelchooser entity plugins.
  modelChooserEntityTypes.forEach((entityType) => {
    const decorators = window.draftailDecorators || {};
    const decorator = decorators[entityType] || DefaultDecorator;
    const plugin = {
      type: entityType,
      source: ModelSource,
      decorator: WrapDecorator(modelChooserDraftailEntities[entityType], decorator),
    };
    window.draftail.registerPlugin(plugin);
  });

  window.draftail.initEditor(widgetAttrIds, draftailOptions, document.currentScript);
};

window.modelChooserDraftailInit = modelChooserDraftailInit;
