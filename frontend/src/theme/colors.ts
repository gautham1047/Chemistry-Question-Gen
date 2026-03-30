export const darkTheme = {
  background: '#545f66',
  highlight: '#829399',
  highlightAlt: '#92b5b2',
  text: '#d5cbcd',
  secondary: '#2f0a28',
};

export const lightTheme = {
  // Placeholder for future light mode implementation
  background: '#ffffff',
  highlight: '#829399',
  highlightAlt: '#92b5b2',
  text: '#000000',
  secondary: '#f5f5f5',
};

export type Theme = typeof darkTheme;

export const theme = darkTheme; // Currently using dark mode only
