/**
 * Utility functions for handling number input and formatting
 * Handles both Portuguese (comma) and English (dot) decimal separators
 */

export const parseFinancialValue = (value) => {
  if (!value || value === '') return 0;
  
  // Convert to string and handle different formats
  let stringValue = String(value).trim();
  
  // Remove currency symbols and spaces
  stringValue = stringValue.replace(/[€$\s]/g, '');
  
  // Handle Portuguese format (comma as decimal separator)
  // If there's both comma and dot, assume comma is decimal separator
  if (stringValue.includes(',') && stringValue.includes('.')) {
    // Format like 1.234.567,89 - remove dots, replace comma with dot
    stringValue = stringValue.replace(/\./g, '').replace(',', '.');
  } else if (stringValue.includes(',')) {
    // Format like 1234,89 - replace comma with dot
    stringValue = stringValue.replace(',', '.');
  }
  // If only dots, assume English format (1234.56)
  
  const parsed = parseFloat(stringValue);
  return isNaN(parsed) ? 0 : parsed;
};

export const formatCurrency = (value, locale = 'pt-PT') => {
  if (value === null || value === undefined || isNaN(value)) return '€0,00';
  
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: 'EUR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
};

export const formatNumber = (value, decimals = 2, locale = 'pt-PT') => {
  if (value === null || value === undefined || isNaN(value)) return '0';
  
  return new Intl.NumberFormat(locale, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
};

export const validateNumericInput = (value, fieldName) => {
  const parsed = parseFinancialValue(value);
  
  if (isNaN(parsed)) {
    return {
      isValid: false,
      error: `O campo "${fieldName}" deve conter um valor numérico válido. Use vírgula (,) ou ponto (.) como separador decimal.`,
      value: 0
    };
  }
  
  return {
    isValid: true,
    error: null,
    value: parsed
  };
};