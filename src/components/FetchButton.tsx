import React from "react";

interface Props {
  onClick: () => void;
}

export const FetchButton: React.FC<Props> = ({ onClick }) => {
  return <button onClick={onClick}>Fetch!!</button>;
};
