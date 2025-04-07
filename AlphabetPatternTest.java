import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class AlphabetPatternTest {
    @Test
    public void testPrintAlphabetPattern() {
        assertEquals("_A_\n_A_B_\n_A_B_C_\n", AlphabetPattern.printAlphabetPattern(3));
        assertEquals("_A_\n_A_B_\n_A_B_C_\n_A_B_C_D_\n", AlphabetPattern.printAlphabetPattern(4));
        assertEquals("_A_\n", AlphabetPattern.printAlphabetPattern(1));
        assertEquals("_A_\n_A_B_\n_A_B_C_\n_A_B_C_D_\n_A_B_C_D_E_\n_A_B_C_D_E_F_\n_A_B_C_D_E_F_G_\n_A_B_C_D_E_F_G_H_\n_A_B_C_D_E_F_G_H_I_\n_A_B_C_D_E_F_G_H_I_J_\n_A_B_C_D_E_F_G_H_I_J_K_\n_A_B_C_D_E_F_G_H_I_J_K_L_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_V_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_V_W_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_V_W_X_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_V_W_X_Y_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_V_W_X_Y_Z_\n", AlphabetPattern.printAlphabetPattern(26));
        assertEquals("_A_\n_A_B_\n_A_B_C_\n_A_B_C_D_\n_A_B_C_D_E_\n_A_B_C_D_E_F_\n_A_B_C_D_E_F_G_\n_A_B_C_D_E_F_G_H_\n_A_B_C_D_E_F_G_H_I_\n_A_B_C_D_E_F_G_H_I_J_\n_A_B_C_D_E_F_G_H_I_J_K_\n_A_B_C_D_E_F_G_H_I_J_K_L_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_\n", AlphabetPattern.printAlphabetPattern(13));
        assertEquals("_A_\n_A_B_\n_A_B_C_\n_A_B_C_D_\n_A_B_C_D_E_\n_A_B_C_D_E_F_\n_A_B_C_D_E_F_G_\n_A_B_C_D_E_F_G_H_\n_A_B_C_D_E_F_G_H_I_\n_A_B_C_D_E_F_G_H_I_J_\n_A_B_C_D_E_F_G_H_I_J_K_\n_A_B_C_D_E_F_G_H_I_J_K_L_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_\n_A_B_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_\n", AlphabetPattern.printAlphabetPattern(20));
    }
}
