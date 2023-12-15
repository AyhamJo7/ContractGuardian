import React, { Component } from "react";
import UploadService from "../services/upload-files.service";
import './Upload.css';


export default class UploadFiles extends Component {
  constructor(props) {
    super(props);
    this.selectFile = this.selectFile.bind(this);
    this.upload = this.upload.bind(this);

    this.state = {
      selectedFiles: undefined,
      currentFile: undefined,
      progress: 0,
      message: "",

      fileInfos: [],
    };
  }

  componentDidMount() {
    UploadService.getFiles().then((response) => {
      this.setState({
        fileInfos: response.data,
      });
    });
  }

  selectFile(event) {
    this.setState({
      selectedFiles: event.target.files,
    });
  }

  upload() {
    let currentFile = this.state.selectedFiles[0];

    this.setState({
      progress: 0,
      currentFile: currentFile,
    });

    UploadService.upload(currentFile, (event) => {
      this.setState({
        progress: Math.round((100 * event.loaded) / event.total),
      });
    })
      .then((response) => {
        this.setState({
          message: response.data.message,
        });
        return UploadService.getFiles();
      })
      .then((files) => {
        this.setState({
          fileInfos: files.data,
        });
      })
      .catch(() => {
        this.setState({
          progress: 0,
          message: "Could not upload the file!",
          currentFile: undefined,
        });
      });

    this.setState({
      selectedFiles: undefined,
    });
  }

  render() {
    const {
      selectedFiles,
      currentFile,
      progress,
      message,
      fileInfos,
    } = this.state;

    return (
      <div className="upload-field">
        {currentFile && (
          <div className="progress">
            <div
              className="progress-bar progress-bar-info progress-bar-striped"
              role="progressbar"
              aria-valuenow={progress}
              aria-valuemin="0"
              aria-valuemax="100"
              style={{ width: progress + "%" }}
            >
              {progress}%
            </div>
          </div>
        )}
        <div className="btn-field">
          <label className="btn btn-default">
            <input type="file" onChange={this.selectFile} />
          </label>

          <button
            className="btn btn-success"
            disabled={!selectedFiles}
            onClick={this.upload}
          >
            Start Scanning
          </button>
        </div>
          <div className="alert alert-light" role="alert">
            {message}
          </div>
        <div className="documents">
          <div className="card">
            <div className="card-header">List of Files</div>
            <ul className="list-group list-group-flush">
              {fileInfos &&
                fileInfos.map((file, index) => (
                  <li className="list-group-item" key={index}>
                    <a href={file.url}>{file.name}</a>
                  </li>
                ))}
            </ul>
          </div>
          <div className="analysis">
            <div className="red-flag dropdown">
              <button className="flag-top dropbtn">
                <h6>{/*amount*/} Red Flags</h6>
                <button>Y</button>
              </button>
            </div>
            <div className="orange-flag dropdown">
              <button className="flag-top dropbtn">
                <h6>{/*amount*/} Orange Flags</h6>
                <button>Y</button>
              </button>
            </div>
            <div className="green-flag dropdown">
              <button className="flag-top dropbtn">
                <h6>{/*amount*/} Green Flags</h6>
                <button>Y</button>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
