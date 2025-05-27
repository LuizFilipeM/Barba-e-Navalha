import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export function Calendar() {
    const { signOut } = useAuth();

    return (
        <>
            <Header
            links={[
            { label: "Home", to: "/" },
            { label: "Agenda", to: "/calendar" },
            { label: "Perfil", to: "/profile" },
            { label: "Sair", onClick: signOut },
            ]}
            />
            <div>
                <h1>Calendario</h1>
            </div>
            <Footer />
        </>
    )
}