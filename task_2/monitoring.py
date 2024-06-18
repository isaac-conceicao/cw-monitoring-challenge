import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import matplotlib.pyplot as plt

def generate_status_report():
    conn = sqlite3.connect('transactions.db')
    current_minute = datetime.now().strftime('%H:%M')

    status_counts = pd.read_sql(f"""
        SELECT 
            status, COUNT(*) as count 
        FROM transactions 
        WHERE time = '{current_minute}' 
        GROUP BY status
    """, conn)

    report = {
        'time': current_minute,
        'approved': status_counts.loc[status_counts['status'] == 'approved', 'count'].values[0],
        'denied': status_counts.loc[status_counts['status'] == 'denied', 'count'].values[0],
        'reversed': status_counts.loc[status_counts['status'] == 'reversed', 'count'].values[0],
        'failed': status_counts.loc[status_counts['status'] == 'failed', 'count'].values[0]
    }

    conn.execute(f"""
        INSERT INTO status_reports (time, approved, denied, reversed, failed) 
        VALUES ('{report['time']}', {report['approved']}, {report['denied']}, {report['reversed']}, {report['failed']})
    """)
    conn.commit()
    conn.close()

    return report

def plot_status_counts():
    conn = sqlite3.connect('transactions.db')
    last_3_minutes = (datetime.now() - timedelta(minutes=3)).strftime('%H:%M')

    reports = pd.read_sql(f"""
        SELECT * FROM status_reports 
        WHERE time >= '{last_3_minutes}'
    """, conn)

    reports.plot(x='time', y=['approved', 'denied', 'reversed', 'failed'], kind='bar')
    plt.show()

    conn.close()

def detect_anomalies(report):
    # Define thresholds for anomalies based on historical data
    thresholds = {
        'approved': 300,
        'denied': 20,
        'reversed': 5,
        'failed': 10
    }

    anomalies = []
    for status, count in report.items():
        if status != 'time' and count > thresholds[status]:
            anomalies.append(status)

    if anomalies:
        send_alert(anomalies)

def send_alert(anomalies):
    msg = MIMEText(f"Anomalies detected in transactions: {', '.join(anomalies)}")
    msg['Subject'] = 'Transaction Anomaly Alert'
    msg['From'] = 'alert@transactions.com'
    msg['To'] = 'team@transactions.com'

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

if __name__ == '__main__':
    report = generate_status_report()
    plot_status_counts()
    detect_anomalies(report)