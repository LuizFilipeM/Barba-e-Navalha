import { StyleCheckBox, StyleCheckBoxInput } from "./style";

export function CheckBox({label, checked, onChange}) {
  return (
    <div style={StyleCheckBox}>
      <input
        type="checkbox"
        checked={checked}
        onChange={onChange}
        style={StyleCheckBoxInput}
      />
      <label style={StyleCheckBox}>{label}</label>
    </div>
  );
}

