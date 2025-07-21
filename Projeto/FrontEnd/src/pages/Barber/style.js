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
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid #007bff;
  color: #007bff;
  background-color: white;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f0f7ff;
  }

  &.primary {
    background-color: #007bff;
    color: white;

    &:hover {
      background-color: #0069d9;
      border-color: #0062cc;
    }
  }
`;

export const ServiceItem = styled.li`
  background: #f8f9fa;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
  
  div {
    display: flex;
    gap: 1rem;
    margin: 0.5rem 0;
  }
  
  p {
    color: #6c757d;
    font-size: 0.9rem;
  }
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
