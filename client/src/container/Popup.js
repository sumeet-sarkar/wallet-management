import React, { Component } from 'react'
import Popup from '../component/popup'

class PopupHandler extends Component {

    state = {
        rows: this.props.modal.rows,
        info: this.props.modal.info
    }

    inputChange = (event) => {

        const rows = [
            ...this.state.rows
        ]
        const info = {
            ...this.state.info
        }
        
        for (let i = 0; i < rows.length; i++){
            if (rows[i].inputName === event.target.name){
                rows[i].inputValue = event.target.value
                info[event.target.name] = event.target.value
                break
            }
        }

        this.setState({
            rows: rows,
            info: info
        })
    }

    render() {
        return(
            <div>
                <Popup
                    title = {this.props.modal.title}
                    rows = {this.state.rows}
                    actionButtonName = {this.props.modal.actionButtonName}
                    cancelButtonName = {this.props.modal.cancelButtonName}
                    info = {this.state.info}
                    inputChange = {(event) => this.inputChange(event)}
                    cancelButton = {
                        this.closeModal,
                        this.props.cancelButton
                    }
                    actionButton = {() => this.props.actionButton(this.state.info)}
                />
            </div>
        )
    }
}

export default PopupHandler