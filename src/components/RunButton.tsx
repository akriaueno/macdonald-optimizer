import React from "react";

interface Props {
  onClick: () => void;
}

export const RunButton: React.FC<Props> = ({ onClick }) => {
  return <button onClick={onClick}>実行</button>;
};
