function Header({ uploadedPDF }) {

  return (

    <div className="header">

      <div>

        <h2>🤖 Nova AI</h2>

        <p>Your Intelligent AI Assistant</p>

      </div>

      {uploadedPDF && (

        <div className="current-pdf">

          📄 {uploadedPDF}

        </div>

      )}

    </div>

  );

}

export default Header;