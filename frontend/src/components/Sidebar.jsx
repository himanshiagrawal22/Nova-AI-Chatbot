function Sidebar({ onNewChat }) {

  return (
    <aside className="sidebar">

      <div className="sidebar-title">
        Nova AI
      </div>

      <button
        className="new-chat-btn"
        onClick={onNewChat}
      >
        + New Chat
      </button>

      <div className="chat-history">

        <div className="chat-history-title">
          Chats
        </div>

      </div>

    </aside>
  );
}

export default Sidebar;