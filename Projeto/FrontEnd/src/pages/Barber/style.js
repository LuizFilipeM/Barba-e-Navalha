import styled from "styled-components";
import { Link } from "react-router-dom";

export const Container = styled.section`
  background-color: #111827;
`;

export const Context = styled.section`
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
`;

export const Title = styled.h1`
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #333;
`;

export const Paragraph = styled.p`
  font-size: 1rem;
  color: #444;
  margin-bottom: 0.5rem;

  strong {
    font-weight: bold;
    color: #222;
  }
`;

export const SubTitle = styled.h3`
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #222;
`;

export const List = styled.ul`
  list-style: none;
  padding-left: 0;

  li {
    padding: 0.4rem 0;
    border-bottom: 1px solid #eee;
    font-size: 1rem;
    color: #555;
  }
`;

export const RegisterLink = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 6rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 2rem auto;
  text-align: center;
`;

export const NotificationTitle = styled.strong`
  color: #dc3545;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
`;

export const RegisterButtons = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
`;

export const RegisterButton = styled(Link)`
  padding: 0.1rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 300;
  transition: all 0.3s ease;
  border: none;
  background-color: #007bff;
  color: white;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #0069d9;
  }
`;

export const DeleteButton = styled.button`
  padding: 5px 10px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin: auto;

  &:hover {
    background-color: #cc0000;
  }
`;

export const ServiceItem = styled.li`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
`;

export const ScheduleItem = styled.li`
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-bottom: 0.5rem;
  
  div {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  
  span {
    background: #e9ecef;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.9rem;
  }
`;

