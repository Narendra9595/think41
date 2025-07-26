import React from "react";
import styles from "./UserInput.module.css";

const UserInput = ({ onSend, inputValue, setInputValue, disabled }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSend(inputValue);
      setInputValue("");
    }
  };

  return (
    <form className={styles.userInput} onSubmit={handleSubmit}>
      <input
        type="text"
        className={styles.input}
        placeholder="Type your message..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        autoFocus
        disabled={disabled}
      />
      <button className={styles.button} type="submit" disabled={disabled}>
        Send
      </button>
    </form>
  );
};

export default UserInput;
