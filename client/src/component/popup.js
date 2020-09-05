import React from 'react';
import "../component/popup.css"

const popup = props => {
    return(
        <div className="modal_bg">
            <form className="modal">
                <h1>{props.title}</h1>
                <div className="modal_body">                    
                    {props.rows.map( row => {
                        return(
                            <div key = {row.inputName}>
                                <label htmlFor={row.inputName}><b>{row.inputName}</b></label>
                                <input 
                                    type={row.inputType}
                                    name={row.inputName}
                                    value={row.inputValue}
                                    onChange={(event) => props.inputChange(event)}
                                    />
                            </div>
                        )
                    })}
                </div>
                <div className="modal_footer">
                    <button type="button" className="cancel_button" onClick={props.cancelButton}>{props.cancelButtonName}</button>
                    <button type="button" className="action_button" onClick={props.actionButton}>{props.actionButtonName}</button>
                </div>
            </form>
        </div>
    )
}

export default popup
