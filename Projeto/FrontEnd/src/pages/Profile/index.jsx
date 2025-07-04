import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";

import { useAuth } from "../../hooks/hookAuth";

import { Header } from "../../components/Header";
import { Button } from "../../components/Button";
import { Footer } from "../../components/Footer";

import { Container, Context, ProfileInfo, ProfileForm } from "./style";

export function Profile() {
    const { signOut, user, setUser } = useAuth();
    const navigate = useNavigate();

    const [isEditing, setIsEditing] = useState(false);

    const [formData, setFormData] = useState({
        name: user.name,
        email: user.email,
        cpf: user.cpf,
        telefone: user.telefone,
        cidade: user.cidade,
        data_nascimento: user.data_nascimento,
        oldPassword: "",
        newPassword: "",
        confirmNewPassword: "",
    });

    function handleChange(e) {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    }

    async function handleUpdate() {
        if (!formData.oldPassword) {
            alert("Por favor, digite sua senha atual para confirmar.");
            return;
        }

        if (formData.newPassword && formData.newPassword !== formData.confirmNewPassword) {
            alert("A nova senha e a confirmação não coincidem.");
            return;
        }

        const response = await api.put(`/api/users/${user.id}`, {
            name: formData.name,
            email: formData.email,
            cpf: formData.cpf,
            telefone: formData.telefone,
            cidade: formData.cidade,
            data_nascimento: formData.data_nascimento,
            oldPassword: formData.oldPassword,
            newPassword: formData.newPassword || null,
        });
        console.log(response.data)
        if (response.data.status === 'success') {
            alert("Dados atualizados com sucesso!");

            const updatedUser = {
                ...user,
                name: formData.name,
                email: formData.email,
                cpf: formData.cpf,
                telefone: formData.telefone,
                cidade: formData.cidade,
                data_nascimento: formData.data_nascimento,
                password: formData.newPassword ? formData.newPassword : formData.oldPassword,
            };

            setUser(updatedUser);
            localStorage.setItem("user", JSON.stringify(updatedUser));

            setIsEditing(false);
            setFormData({ ...formData, oldPassword: "", newPassword: "", confirmNewPassword: "" });
            navigate("/");
        } else {
            alert("Erro ao atualizar dados: " + response.data.message   );
        }
    }


    async function handleDeleteAccount() {
        const confirmDelete = window.confirm(
            "Tem certeza que deseja excluir sua conta? Esta ação não pode ser desfeita."
        );

        if (confirmDelete) {
            const response = await api.delete(`/api/users/${user.id}`);
            if (response.data.status === 'success') {
                alert("Conta excluída com sucesso.");
                signOut();
            } else {
                alert("Erro ao excluir a conta.");
            }
        }
    }

    return (
        <Container>
            <Header
                links={[
                    { label: "Home", to: "/" },
                    { label: "Perfil", to: "/profile" },
                    { label: "Sair", onClick: signOut },
                ]}
            />

            <Context>
                <h1>Meu Perfil</h1>

                {!isEditing ? (
                    <ProfileInfo>
                        <p><strong>Tipo:</strong> {user.tipo}</p>
                        <p><strong>Nome:</strong> {user.name}</p>
                        <p><strong>Email:</strong> {user.email}</p>
                        <p><strong>CPF:</strong> {user.cpf}</p>
                        <p><strong>Telefone:</strong> {user.telefone}</p>
                        <p><strong>Cidade:</strong> {user.cidade}</p>
                        <p><strong>Data de Nascimento:</strong> {user.data_nascimento}</p>

                        <Button onClick={() => setIsEditing(true)} title="Editar Dados"/>
                        <Button onClick={handleDeleteAccount} title="Excluir Conta"/>
                    </ProfileInfo>
                ) : (
                    <ProfileForm>
                        <label>
                            Nome:
                            <input
                                type="text"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                            />
                        </label>

                        <label>
                            CPF:
                            <input
                                type="number"
                                name="cpf"
                                value={formData.cpf}
                                style={{ backgroundColor: 'rgb(166, 168, 173)', color: 'black' }}
                            />
                        </label>

                        <label>
                            Telefone:
                            <input
                                type="number"
                                name="telefone"
                                value={formData.telefone}
                                onChange={handleChange}
                            />
                        </label>

                        <label>
                            Cidade:
                            <input
                                type="text"
                                name="cidade"
                                value={formData.cidade}
                                onChange={handleChange}
                            />
                        </label>

                        <label>
                            Data de Nascimento:
                            <input
                                type="date"
                                name="data_nascimento"
                                value={formData.data_nascimento}
                                style={{ backgroundColor: 'rgb(166, 168, 173)', color: 'black' }}
                            />
                        </label>

                        <hr />

                        <label>
                            Email:
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                            />
                        </label>

                        <label>
                            <strong>Senha Atual:</strong>
                            <input
                                type="password"
                                name="oldPassword"
                                value={formData.oldPassword}
                                onChange={handleChange}
                                placeholder="Digite sua senha atual para confirmar a alteração."
                                required
                            />
                        </label>

                        <label>
                            Nova Senha:
                            <input
                                type="password"
                                name="newPassword"
                                value={formData.newPassword}
                                onChange={handleChange}
                                placeholder="Digite uma nova senha, ou deixe em branco para manter a senha atual."
                            />
                        </label>

                        <label>
                            Confirmar Nova Senha:
                            <input
                                type="password"
                                name="confirmNewPassword"
                                value={formData.confirmNewPassword}
                                onChange={handleChange}
                                placeholder="Confirme a nova senha."
                            />
                        </label>

                        <Button onClick={handleUpdate} title={"Salvar Alterações"}/>
                        <Button onClick={() => setIsEditing(false)} title={"Cancelar"}/>
                    </ProfileForm>
                )}
            </Context>

            <Footer />
        </Container>
    );
}
