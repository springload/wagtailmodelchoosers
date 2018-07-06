import React from 'react';

const GenericModelEntity = (props) => {
  console.log(props);
  return React.createElement(
    'span',
    {
      // TODO: Use key to match Python handlers (it has to be unique per entity).
      // TODO: Set data correctly.
      'data-foo': 'test',
    },
    props.children,
  );
};

export default GenericModelEntity;
