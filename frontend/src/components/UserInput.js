import React, { useState } from "react";
import styles from "./UserInput.module.css";

const UserInput = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <form className={styles.userInput} onSubmit={handleSubmit}>
      <input
        type="text"
        className={styles.input}
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        autoFocus
      />
      <button className={styles.button} type="submit">
        Send
      </button>
    </form>
  );
};

export default UserInput;
