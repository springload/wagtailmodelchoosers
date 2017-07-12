
// Translation function.
export const tr = (defaultTranslations, customTranslations, key) => {
  if (customTranslations && key in customTranslations) {
    return customTranslations[key];
  }

  if (key in defaultTranslations) {
    return defaultTranslations[key];
  }

  return key.replace(/_/g, ' ');
};

export const pluralize = (
  defaultTranslations,
  customTranslations,
  singularKey,
  pluralKey,
  count,
) => {
  const singular = tr(defaultTranslations, customTranslations, singularKey);
  const plural = tr(defaultTranslations, customTranslations, pluralKey);

  return count === 1 ? singular : plural;
};
