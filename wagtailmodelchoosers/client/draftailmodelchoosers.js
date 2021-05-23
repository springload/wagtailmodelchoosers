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

  // Go through all draftail entities and for all the modelchooser ones, make the icon name
  // into a <span> tag and put the 'icon' string into the class.  This is the only way
  // to get fontawesome icons working in draftail, which expects SVG icons.
  draftailOptions.entityTypes = draftailOptions.entityTypes.map((et) => {
    const _icon = modelChooserEntityTypes.includes(et.type)
      ? window.React.createElement('span', { class: `icon ${et.icon}` })
      : et.icon;
    return Object.assign(et, { icon: _icon, icon_name: et.icon });
  });

  window.draftail.initEditor(widgetAttrIds, draftailOptions, document.currentScript);
};

window.modelChooserDraftailInit = modelChooserDraftailInit;
