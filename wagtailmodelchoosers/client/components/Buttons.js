import PropTypes from 'prop-types';
import React from 'react';

const Button = ({ isActive, classes, label, onClick }) => {
  const buttonClasses = classes.slice();

  buttonClasses.push('button');
  if (!isActive) {
    buttonClasses.push('button--disabled');
  }

  return (
    <button
      type="button"
      onClick={onClick}
      className={buttonClasses.join(' ')}
    >
      {label}
    </button>
  );
};

Button.defaultProps = {
  isActive: true,
  classes: [],
};

Button.propTypes = {
  isActive: PropTypes.bool,
  classes: PropTypes.arrayOf(PropTypes.string),
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

const CloseButton = ({ onClick }) => {
  const classes = ['close', 'icon', 'text-replace', 'icon-cross'];

  return <Button classes={classes} onClick={onClick} label="x" />;
};

CloseButton.propTypes = {
  onClick: PropTypes.func.isRequired,
};

const SecondaryButton = ({ label, onClick }) => {
  const classes = ['action-choose', 'button-small', 'button-secondary'];

  return <Button classes={classes} onClick={onClick} label={label} />;
};

SecondaryButton.propTypes = {
  label: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default Button;
export {
  CloseButton,
  SecondaryButton,
};
