import React from 'react'
import './rows.css'

const rows = props => {

    return(
        <table>

            <thead>
                <tr>                    
                    {props.columnNames.map(columnName => {
                        return(
                            <th key={columnName}>{columnName}</th>
                        )
                    })}
                </tr>
            </thead>

            <tbody>
                {props.dataRows.map( dataRow => {
                    return(
                        <tr onClick={() => props.rowClicked(dataRow.id)} key={dataRow.id}>
                            {props.columnNames.map(columnName => {
                                return(
                                    <td key={dataRow[columnName]}>{dataRow[columnName]}</td>
                                )
                            })}
                            <td onClick={(event) => {
                                event.stopPropagation()
                                props.performAction(dataRow,"Edit")
                            }}>Edit</td>
                            <td onClick={(event) => {
                                event.stopPropagation()
                                props.performAction(dataRow, "Delete")
                            }}>Delete</td>
                        </tr>
                    )
                })}
            </tbody>
        </table>
    )
}

export default rows;
