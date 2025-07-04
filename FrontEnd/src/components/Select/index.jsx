import { StyleSelect, StyleInput, StyleLabel } from "./style";

export function Select({label, options, onChange}) {
  return (
    <div style={StyleSelect}>
      {label && <label style={StyleLabel}>{label}</label>}
      <select style={StyleInput} onChange={onChange}>
        <option value=""></option>
        {options.map(option => (
          <option key={option.value} value={option.value}>{option.label}</option>
        ))}
      </select>
    </div>
  );
}

