function X = GenerateSheppLogans(Nimg, Nsize, sigma)
%GENERATESHEPPLOGANS Generaing multiple shapplogan phantoms.
%Suggest sigma = 0.1, plotwindow = [0.9 1.1]
Em = zeros(10, 6);
Em(:,1) = [2 -0.98 -0.02 0.02 0.01 0.01 0.01 0.01 0.01 0.01]';
Em(:,2) = [0.69 0.6624 0.11 0.16 0.21 0.046 0.046 0.046 0.023 0.023]';
Em(:,3) = [0.92 0.874 0.31 0.41 0.25 0.046 0.046 0.023 0.023 0.046]';
Em(:,4) = [0 0 .22 -.22 0 0 0 -.08 0 .06]';
Em(:,5) = [0 -.0184 0 0 .35 .1 -.1 -.605 -.605 -.605]';
Em(:,6) = [0 0 -18 18 0 0 0 0 0 0]';
sigmac = [0.1, 1, 1, 1, 1, 10];
X = zeros(Nsize, Nsize, Nimg);
for i = 1 : Nimg
    E = randn(10,6);    
    E = E.*Em*sigma;
    for j = 1 : 6
        E(:,j) = E(:, j) * sigmac(j);
    end
    E = E + Em;
    img = phantom(E, Nsize);
    img = imrotate(img, sigma*10*randn(),'crop');
%     img = reshape(img, Nsize*Nsize, 1);
    X(:,:,i) = img;    
end
end

