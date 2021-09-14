%% Setup
close all;
clear all;

rng(1,'twister') %シード=0の時、逆行列の推定?

%% 入力・出力画素値
f_nx=8;f_ny=8;
g_nx=20;g_ny=20;

% 波長
N_wavelength=3;

% シフト量
shift_row=0
shift_column=1

pre_sampling=1000;
pre_iterations=3000;

%% SLMでの変調パターン
F_com_matrix=randi([0,1],f_nx,f_ny,pre_sampling);
% シフト確認するときはzerosに変更する
% F_matrix_2D=randi([0,1],f_nx,f_ny,pre_sampling,N_wavelength);
F_matrix_2D=randi([0,1],f_nx,f_ny,pre_sampling,N_wavelength);
F_matrix=randi([0,1],f_nx*f_ny,pre_sampling,N_wavelength);

% 重複箇所
figure;
subplot(1,2,1);imagesc(abs(F_com_matrix(:,:,1)));axis image;colorbar;title("com");
subplot(1,2,2);imagesc(angle(F_com_matrix(:,:,1)));axis image;colorbar;title("com");
drawnow

% 重複箇所をシフト
for k=1:N_wavelength
    F_matrix_2D(1+shift_row*(k-1):f_nx,1+shift_column*(k-1):f_ny,:,k)=F_com_matrix(1:(f_nx-(shift_row*(k-1))),1:(f_ny-(shift_column*(k-1))),:);
    F_matrix(:,:,k)=reshape(F_matrix_2D(:,:,:,k), [f_nx*f_ny,pre_sampling]);
end

% 出力
figure;
for k = 1:N_wavelength
    subplot(N_wavelength,2,2*k-1);imagesc(reshape(abs(F_matrix(:,2,k)),[f_nx,f_ny]));axis image;colorbar;title("shift F abs "+string(k));
    subplot(N_wavelength,2,2*k);imagesc(reshape(angle(F_matrix(:,2,k)),[f_nx,f_ny]));axis image;colorbar;title("shift F angle "+string(k));
end
drawnow;

%% MSTM推定
% 変数生成
MSTM=zeros(g_nx*g_ny,f_nx*f_ny,N_wavelength);
MSTM_estimate=zeros(g_nx*g_ny,f_nx*f_ny,N_wavelength);
G_matrix=zeros(g_nx*g_ny,pre_sampling,N_wavelength);
G_matrix_intensity=zeros(g_nx*g_ny,pre_sampling);
Inverse_F_matrix=zeros(pre_sampling,f_nx*f_ny, N_wavelength);
G_matrix_estimate_amplitude=zeros(g_nx*g_ny,pre_sampling,N_wavelength);
G_matrix_estimate_theta=zeros(g_nx*g_ny,pre_sampling,N_wavelength);
G_matrix_estimate_amplitude_rate=zeros(g_nx*g_ny,pre_sampling,N_wavelength);
G_matrix_estimate=zeros(g_nx*g_ny,pre_sampling,N_wavelength);
Err_abs_TM_RMSE=zeros(1,pre_iterations,N_wavelength);
G_matrix_estimate_intensity=zeros(g_nx*g_ny,pre_sampling);

%% 代入
for c=1:N_wavelength
    MSTM(:,:,c)=rand(g_nx*g_ny,f_nx*f_ny).*exp(1i*2*pi*rand(g_nx*g_ny,f_nx*f_ny));
    Inverse_F_matrix(:,:,c)=pinv(F_matrix(:,:,c));
    % 初期推定出力振幅
    G_matrix_estimate_amplitude(:,:,c)=rand(g_nx*g_ny,pre_sampling);
    % 初期推定出力位相 
    G_matrix_estimate_theta(:,:,c)=2*pi*rand(g_nx*g_ny,pre_sampling);
    % 初期推定出力
    G_matrix_estimate(:,:,c)=G_matrix_estimate_amplitude(:,:,c).*exp(1i*G_matrix_estimate_theta(:,:,c));
    Err_abs_TM_RMSE(:,:,c)=zeros(1,pre_iterations);
    % 出力真値
    G_matrix(:,:,c)=MSTM(:,:,c)*F_matrix(:,:,c);
    % 計測強度和
    G_matrix_intensity=G_matrix_intensity+(abs(G_matrix(:,:,c))).^2;
end

G_matrix_amplitude=sqrt(G_matrix_intensity);

%% 反復過程 
for r = 1:pre_iterations
    %各波長推定強度和
    for c=1:N_wavelength
       G_matrix_estimate_intensity=G_matrix_estimate_intensity + abs(G_matrix_estimate(:,:,c)).^2; 
    end
    
    for c=1:N_wavelength
        % 振幅抽出
        G_matrix_estimate_amplitude(:,:,c)=abs(G_matrix_estimate(:,:,c));
        % 位相抽出
        G_matrix_estimate_theta(:,:,c)=angle(G_matrix_estimate(:,:,c));
        % 振幅比(推定出力振幅/推定合成波振幅)
        G_matrix_estimate_amplitude_rate(:,:,c)=G_matrix_estimate_amplitude(:,:,c)./sqrt(G_matrix_estimate_intensity);
        % 振幅更新
        G_matrix_estimate_amplitude(:,:,c)=G_matrix_amplitude.*G_matrix_estimate_amplitude_rate(:,:,c);
        % 出力更新(計測合成波振幅*振幅*位相)
        G_matrix_estimate(:,:,c)=G_matrix_estimate_amplitude(:,:,c).*exp(1i*G_matrix_estimate_theta(:,:,c));
        % TM推定
        MSTM_estimate(:,:,c)=G_matrix_estimate(:,:,c)*Inverse_F_matrix(:,:,c);
        % 順伝搬
        G_matrix_estimate(:,:,c)=MSTM_estimate(:,:,c)*F_matrix(:,:,c);
        % RMSE 
        Err_abs_TM_RMSE(:,r,c)=immse(abs(MSTM_estimate(:,:,c)), abs(MSTM(:,:,c))); 
    end
    G_matrix_estimate_intensity=zeros(g_nx*g_ny,pre_sampling);
end

%% 推定TM
figure;
for k = 1:N_wavelength
    subplot(N_wavelength,2,2*k-1);imagesc(abs(MSTM(:,:,k)));axis image;colorbar;title("MSTM "+string(k));
    subplot(N_wavelength,2,2*k);imagesc(abs(MSTM_estimate(:,:,k)));axis image;colorbar;title("MSTM estimate "+string(k));
end
drawnow;

%% TM RMSE
figure;
for k = 1:N_wavelength
    subplot(1,N_wavelength,k);semilogy(Err_abs_TM_RMSE(:,:,k)); title("MSTM RMSE "+string(k));xlabel ("epoch");ylabel("RMSE");
end
drawnow;


%% 逆伝搬
post_iterations=4000;

% 変数生成
f_vector=zeros(f_nx,f_ny);
g_vector=zeros(g_nx*g_ny,1);
g_vector_amplitude=zeros(g_nx*g_ny,1);
g_vector_theta_estimate=zeros(g_nx*g_ny,1);
g_vector_estimate=zeros(g_nx*g_ny,1);
Inverse_MSTM_estimate=zeros(f_nx*f_ny,g_nx*g_ny);
Err_abs_f_RMSE=zeros(1,post_iterations);

% 位相変調
for c=1:N_wavelength
    f_vector(:,:,c)=zeros(f_nx,f_ny);
    f_vector(int32(f_nx*0.1*c):int32(f_nx*0.2*c),int32(f_nx*0.1*c):int32(f_nx*0.2*c),c)=1;
end

% 代入
for c=1:N_wavelength
    g_vector(:,:,c)=MSTM(:,:,c)*reshape(f_vector(:,:,c),[f_nx*f_ny,1]);
    g_vector_amplitude(:,:,c)=abs(g_vector(:,:,c));
    g_vector_theta_estimate(:,:,c)=2*pi*rand(g_nx*g_ny,1);
    g_vector_estimate(:,:,c)=g_vector_amplitude(:,:,c).*exp(1i*g_vector_theta_estimate(:,:,c));
    Inverse_MSTM_estimate(:,:,c)=pinv(MSTM_estimate(:,:,c));
    Err_abs_f_RMSE(:,:,c)=zeros(1,post_iterations);
end

%% 反復過程
% 推定したTMの逆行列からfを推定→推定したTMで順伝搬→推定したg_vectorの振幅を置換→TMの逆行列から..を繰り返す
f_vector_estimate=zeros(f_nx*f_ny,1);
for r = 1:post_iterations
    for c=1:N_wavelength
        % 逆伝搬
        f_vector_estimate(:,:,c)=Inverse_MSTM_estimate(:,:,c)*g_vector_estimate(:,:,c);
        % 順伝搬
        g_vector_estimate(:,:,c)=MSTM_estimate(:,:,c)*f_vector_estimate(:,:,c);
        % 位相抽出
        g_vector_theta_estimate(:,:,c)=angle(g_vector_estimate(:,:,c));
        % 更新
        g_vector_estimate(:,:,c)=g_vector_amplitude(:,:,c).*exp(1i*g_vector_theta_estimate(:,:,c));
        % RMSE 
        Err_abs_f_RMSE(:,r,c)=immse(abs(f_vector_estimate(:,:,c)), abs(reshape(f_vector(:,:,c),[f_nx*f_ny,1])));
    end
end    

%%
% 振幅
figure;
for k = 1:N_wavelength
    subplot(N_wavelength,2,2*k-1);imagesc(abs(reshape(f_vector(:,:,k), [f_nx,f_ny])));axis image;colorbar;title("abs true ");
    subplot(N_wavelength,2,2*k);imagesc(abs(reshape(f_vector_estimate(:,:,k), [f_nx,f_ny])));axis image;colorbar;title("abs estimate ");
end
drawnow;

% 位相
figure;
for k = 1:N_wavelength
    subplot(N_wavelength,2,2*k-1);imagesc(angle(reshape(f_vector(:,:,k), [f_nx,f_ny])));axis image;colorbar;title("phase true ");
    subplot(N_wavelength,2,2*k);imagesc(angle(reshape(f_vector_estimate(:,:,k), [f_nx,f_ny])));axis image;colorbar;title("phase estimate ");
end
drawnow;

% RMSE
figure;
for k = 1:N_wavelength
    subplot(1,N_wavelength,k);semilogy(Err_abs_f_RMSE(:,:,k)); title("f RMSE ");xlabel ("epoch");ylabel("RMSE");
end
drawnow;