import React, { useState, useEffect } from 'react';
import styles from './SidePanel.module.css';

const SidePanel = ({ userId }) => {
  const [userInfo, setUserInfo] = useState({
    name: 'John Doe',
    email: 'john.doe@example.com',
    memberSince: '2023',
    totalOrders: 12
  });

  const [recentOrders, setRecentOrders] = useState([
    { id: 'ORD-001', status: 'Delivered', date: '2024-01-15', total: '$89.99' },
    { id: 'ORD-002', status: 'In Transit', date: '2024-01-20', total: '$124.50' },
    { id: 'ORD-003', status: 'Processing', date: '2024-01-25', total: '$67.25' }
  ]);

  const faqs = [
    {
      question: "How do I track my order?",
      answer: "You can track your order by entering your order number in the tracking section."
    },
    {
      question: "What's your return policy?",
      answer: "We offer 30-day returns for most items. Some restrictions apply."
    },
    {
      question: "Do you ship internationally?",
      answer: "Yes, we ship to most countries. Shipping costs and delivery times vary."
    },
    {
      question: "How can I change my order?",
      answer: "Contact us within 2 hours of placing your order for modifications."
    }
  ];

  const [expandedFaq, setExpandedFaq] = useState(null);

  const getStatusColor = (status) => {
    switch (status) {
      case 'Delivered': return '#10b981';
      case 'In Transit': return '#3b82f6';
      case 'Processing': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  return (
    <div className={styles.sidePanel}>
      {/* User Info Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>👤 Customer Info</h3>
        <div className={styles.userCard}>
          <div className={styles.userAvatar}>
            {userInfo.name.charAt(0)}
          </div>
          <div className={styles.userDetails}>
            <h4>{userInfo.name}</h4>
            <p>{userInfo.email}</p>
            <div className={styles.userStats}>
              <span>Member since {userInfo.memberSince}</span>
              <span>{userInfo.totalOrders} orders</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Orders Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>📦 Recent Orders</h3>
        <div className={styles.ordersList}>
          {recentOrders.map((order) => (
            <div key={order.id} className={styles.orderItem}>
              <div className={styles.orderHeader}>
                <span className={styles.orderId}>{order.id}</span>
                <span 
                  className={styles.orderStatus}
                  style={{ color: getStatusColor(order.status) }}
                >
                  {order.status}
                </span>
              </div>
              <div className={styles.orderDetails}>
                <span className={styles.orderDate}>{order.date}</span>
                <span className={styles.orderTotal}>{order.total}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* FAQs Section */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>❓ Quick Help</h3>
        <div className={styles.faqList}>
          {faqs.map((faq, index) => (
            <div key={index} className={styles.faqItem}>
              <button
                className={styles.faqQuestion}
                onClick={() => setExpandedFaq(expandedFaq === index ? null : index)}
              >
                <span>{faq.question}</span>
                <span className={styles.faqArrow}>
                  {expandedFaq === index ? '▼' : '▶'}
                </span>
              </button>
              {expandedFaq === index && (
                <div className={styles.faqAnswer}>
                  {faq.answer}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className={styles.section}>
        <h3 className={styles.sectionTitle}>⚡ Quick Actions</h3>
        <div className={styles.quickActions}>
          <button className={styles.actionBtn}>
            📋 Track Order
          </button>
          <button className={styles.actionBtn}>
            🔄 Start Return
          </button>
          <button className={styles.actionBtn}>
            💳 Payment Info
          </button>
          <button className={styles.actionBtn}>
            📞 Contact Us
          </button>
        </div>
      </div>
    </div>
  );
};

export default SidePanel; 