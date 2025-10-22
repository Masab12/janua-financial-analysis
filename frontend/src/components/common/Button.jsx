import React from 'react';

const Button = ({ children, onClick, type = 'button', variant = 'primary', disabled = false, fullWidth = false }) => {
  const baseClass = fullWidth ? 'w-full' : '';
  const variantClass = variant === 'primary' ? 'btn-primary' : 'btn-secondary';
  const disabledClass = disabled ? 'opacity-50 cursor-not-allowed' : '';
  
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClass} ${variantClass} ${disabledClass}`}
    >
      {children}
    </button>
  );
};

export default Button;
