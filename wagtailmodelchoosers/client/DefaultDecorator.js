import PropTypes from 'prop-types';
import React from 'react';

const DefaultDecorator = (entityData, props) => {
  const { entityKey, contentState, children } = props;
  const d = contentState.getEntity(entityKey).getData();
  const { id } = d;

  const prefixLabel = entityData.prefix_label || '';
  const prefix = `#${id} ${prefixLabel} - `;

  return (
    <span data-tooltip={entityKey} className="RichEditor-link">
      {entityData.icon}
      {prefix}
      {children}
    </span>
  );
};

DefaultDecorator.propTypes = {
  entityKey: PropTypes.string.isRequired,
  contentState: PropTypes.object.isRequired,
  children: PropTypes.node.isRequired,
};

export default DefaultDecorator;
