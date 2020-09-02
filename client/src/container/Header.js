import React, { Component } from 'react';
import { connect } from 'react-redux';
import * as actionTypes from '../store/actions'

import "./Header.css"

class Header extends Component{

    notes = () => {
        return(
            <>
                {this.props.ctr}
                <button onClick={this.props.onIncrementCounter}>
                Inc.
                </button>
                <button onClick={() => this.props.onAddArray(this.props.ctr)}>
                Add.
                </button>
                <button onClick={() => this.props.onDelArray((id) => this.props.ctr(id))}>
                Del.
                </button>
            </>
        )
    }

    render() {
        console.log(this.props.ctr)
        console.log(this.props.storedResults)
        return(
            <div className="global_nav">
                <div className="user">
                    My Profile
                </div>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        ctr: state.counter,
        storedResults: state.results
    };
}

const mapDispatchToProps = dispatch => {
    return {
        onIncrementCounter: () => dispatch({type: actionTypes.INC_COUNTER }),
        onDelArray: (id) => dispatch({type: actionTypes.DEL_ARRAY, resultElId: id}),
        onAddArray: () => dispatch({type: actionTypes.ADD_ARRAY})
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);