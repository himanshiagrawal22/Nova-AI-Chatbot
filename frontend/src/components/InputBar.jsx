
function InputBar({
  message,
  setMessage,
  sendMessage,
  loading,
  uploading,
  uploadedPDF,
  handlePDFUpload,
  handleRemovePDF,
}) {
  return (
    <div className="composer">

      {uploadedPDF && (
        <div className="attachment">

          <div className="attachment-left">
            📄
            <span>{uploadedPDF}</span>
          </div>

          <button
            onClick={handleRemovePDF}
            className="attachment-remove"
          >
            ✕
          </button>

        </div>
      )}

      <div className="composer-row">

        <input
          type="file"
          hidden
          id="pdfUpload"
          accept=".pdf"
          onChange={(e) => {
            handlePDFUpload(e.target.files[0]);
            e.target.value = "";
          }}
        />

        <label
          htmlFor={!uploading ? "pdfUpload" : ""}
          className={`attach-button ${uploading ? "disabled" : ""}`}
        >
          {uploading ? "⏳" : "📎"}
        </label>

        <input
          className="message-input"
          placeholder={
            uploadedPDF
              ? `Ask about ${uploadedPDF}...`
              : "Ask Nova anything..."
          }
          value={message}
          disabled={loading}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button
          className="send-button"
          disabled={loading || message.trim() === ""}
          onClick={sendMessage}
        >
          {loading ? "..." : "➤"}
        </button>

      </div>

    </div>
  );
}

export default InputBar;