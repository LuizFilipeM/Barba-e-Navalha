import styled from "styled-components"

export const Container = styled.main`
  background-color:  #111827;
`

export const Content = styled.div`
  max-width: 1008px;
  height: 82vh;
  margin: auto;

  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;

  > img {
    width: 20rem;
  }

  > div {
    text-align: center;

    > h1 {
      font-size: 2.5rem;
      margin-bottom: 0.625rem;

      color:  #f9f9f9;
    }

    > p {
      font-size: 1.5rem;

      margin-bottom: 0.625rem;
      color:  #f9f9f9;
    }
  }
`
