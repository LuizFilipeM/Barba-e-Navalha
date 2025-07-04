import { StyleButton } from "./style"

export function Button({title, onClick}) {
  return (
      <button style={StyleButton} onClick={onClick} >{title}</button>
  )
}
