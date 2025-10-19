import React from 'react';

const Input = ({ label, value, onChange, name, type = 'number', required = false, error }) => {
  return (
    <div className="mb-4">
      <label htmlFor={name} className="label-text">
        {label}
        {required && <span className="text-janua-orange ml-1">*</span>}
      </label>
      <input
        type={type}
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        className={`input-field ${error ? 'border-red-500 focus:ring-red-500' : ''}`}
        step={type === 'number' ? '0.01' : undefined}
      />
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
};

export default Input;
