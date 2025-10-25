import React from 'react';

const Card = ({ title, children, className = '', action = null }) => {
  return (
    <div className={`card ${className}`}>
      {title && (
        <div className="flex items-center justify-between mb-4">
          <h3 className="section-title mb-0">{title}</h3>
          {action && <div className="ml-4">{action}</div>}
        </div>
      )}
      {!title && action && (
        <div className="flex justify-end mb-4">
          {action}
        </div>
      )}
      {children}
    </div>
  );
};

export default Card;
