import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Footer } from "../../components/Footer";

export function Schedule() {
    const { signOut } = useAuth();

    return (
        <>
            <Header
            links={[
            { label: "Home", to: "/" },
            { label: "Perfil", to: "/profile" },
            { label: "Sair", onClick: signOut },
            ]}
            />
            <div>
                <h1>Horarios</h1>
            </div>
            <Footer />
        </>
    )
}