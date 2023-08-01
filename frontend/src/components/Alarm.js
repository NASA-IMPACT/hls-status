import formatDate from '../utilities/date';
import '../styles/Alarm.css';

function Alarm({ alarm }) {

  return (
    <div className="alarm-container">
      {Object.keys(alarm).map((alarmKey) => (
        <div key={alarmKey} className="alarm-item">
          <div className="alarm-header">
            <div className="alarm-details">
              <h3 className="alarm-title">{alarmKey}</h3>
              <div className="alarm-timestamp">{formatDate(alarm[alarmKey].state_updated_timestamp)}</div>
            </div>
          </div>
          <div className="status-icon" title={alarm[alarmKey].state}>
            {alarm[alarmKey].state === 'OK' ? (
              <i className="fas fa-check-circle ok-icon"></i>
            ) : alarm[alarmKey].state === 'ALARM' ? (
              <i className="fas fa-exclamation-triangle danger-icon"></i>
            ) : alarm[alarmKey].state === 'INSUFFICIENT_DATA' ? (
              <i className="fas fa-solid fa-exclamation-circle alert-icon"></i>
            ) : null}
          </div>
        </div>
      ))}
    </div>
  );
}

export default Alarm;
