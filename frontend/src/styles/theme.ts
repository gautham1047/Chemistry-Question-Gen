// Centralized reusable styles for Chemistry Question Gen
// Sharp rectangular borders, sleek dark palette, high contrast

export const styles = {
  // Layout containers
  container: 'max-w-5xl w-full mx-auto px-4 py-8',
  containerWide: 'max-w-6xl w-full mx-auto px-4 py-8',

  // Box / Card containers (sharp rectangular edges, zero rounded borders)
  card: 'bg-slate-800 border border-slate-700 p-6 shadow-sm',
  cardSm: 'bg-slate-800 border border-slate-700 p-4 shadow-sm',
  cardEmerald: 'bg-emerald-950/30 border border-emerald-500/40 p-5 shadow-sm',

  // Section headers and text
  heading: 'text-xl font-bold text-slate-100',
  subheading: 'text-xs text-slate-400',
  sectionTitle: 'text-xs font-semibold uppercase tracking-wider text-cyan-400',

  // Badges (zero rounded borders)
  badgeCyan: 'font-mono text-xs uppercase tracking-wider text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-2 py-0.5',
  badgeSlate: 'text-xs text-slate-400 bg-slate-700/50 px-2 py-0.5',
  badgeEmerald: 'font-mono text-xs uppercase tracking-wider text-emerald-400 bg-emerald-950/60 border border-emerald-800/40 px-2 py-0.5',

  // Inputs & forms (zero rounded borders)
  input: 'w-full px-3 py-1.5 bg-slate-800 border border-slate-700 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500',
};
