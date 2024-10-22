function [res_smoothed,res_std,pos, n ] = AethSmoothing( RealTime,res,ATN,varargin )
% AethSmoothing smooths aethalometer data based on Pikridas et al., 2019,
% which in turn was based on 
% Hagler, G.: Post-processing Method to Reduce Noise while Preserving High
% Time Resolution in Aethalometer Real-time Black Carbon Data, Aerosol Air
% Qual Res, doi:10.4209/aaqr.2011.05.0055, 2011.
% The algorithm uses uncorrected data (no Weigartner or any other correction) 
% as delivered by the instrument or calculated by the user. Only
% homogeneous timeseries are considered.
% The original code by Hagler et al. can be found in the supplementary info
% of the paper cited above. It is written in matlab as well.
%
%     Syntax:
% [response_smoothed,response_std,positions, NumberOfPoints ] = AethSmoothingUpload(Time,Reponse,Attenuation);
%
%   Inputs:
%      Time, Mx1 vector.  Time of the data in julian format, ie 1 = one day
%      Response, Mx1 matrix  The response to be smoothed, it can be babs or BC mass in any units
%      Attenuation, same size as Response. The attenuation as provided by the instrument or calculated by the user (Important read note below). This
%      input must have enough accuracy for the function to operate
%      properly. 4 decimal accuracy is optimal. 3 decimal accuracy will
%      suffice in most cases.
%      
%      VARARGIN:
%
%       'method', the method to use for smoothing. Possible options are
%         {'moving'}
%         'lowess'
%          'sgolay'
%         'average'
%             The moving method is better tested. The lowess method is very
%          problematic. The average method will smooth similar to the
%          original ONA algorithm based on the reference above (ie by Hagler et al., 2011).
%
%       'ATNincrement', A number below unity. Arranges the intensity of the smoothing. The
%               greater the value the more intense the smoothing. A default value
%               of 0.05 is used if the increment is not set.
%
%       'Weights', {0} or 1. This parameter is only valid if the moving method is
%               used. In case the sample has large variations in the concentration
%               of BC the method may yield unrealistic results. Applying weights
%               eliminates such problems. However, applying weights may increase
%               the effect of outliers. So it is advised for both the normal and
%               weighed method to be used in parallel. Applying weights will
%               distort the edges (begining and end) of your time series.
%
%   Output:
%      response_smoothed,   The reponse smoothed based on ATNincrement
%      response_std,   one standard deviation of the smoothed response
%      positions, the positions of the data smoothed. This output helps
%      duplicate the result. However, when you use weights you cannot duplicate the result 
%
%
%      NumberOfPoints, how many data points were used for each average.
%
% %   Example:
%      [smooth_moving,smooth_moving_std,smooth_moving_pos,smooth_moving_np ] = AethSmoothing(Time,babs,Attennuation);
% % the above statement is equals to
%      [smooth_moving,smooth_moving_std,smooth_moving_pos,smooth_moving_np ]...
% = AethSmoothing(Time,babs,Att,'method','moving','ATNincrement',0.05,'Weights',0);
%
% [smooth_moving,smooth_moving_std,smooth_moving_pos,smooth_moving_np ] = AethSmoothing(Time,babs,Attennuation, 'Weights',1);
% will do the same but now weights are applied.
%
% % [smooth_moving,smooth_moving_std,smooth_moving_pos,smooth_moving_np ] = AethSmoothing(Time,babs,Attennuation, 'ATNincrement',0.01);
% reduces the ATN increment to 0.01 from 0.05, which is the default.
% 
% 
% Time=(1:numel(Att))/(24*60*60);
% babs=50+sin(0:pi/500:2*pi)+.9*(rand(1,1001)-.5);
% Att=babs*100*1.7/7.1;
% [smooth_moving,smooth_moving_std,smooth_moving_pos,smooth_moving_np ] = AethSmoothing(Time',babs',Att');
% plot(Time,babs,'ok','MarkerFaceColor','k')
% hold on
% plot(Time,smooth_moving,'-r','LineWidth',3)
% hold off
% datetick('x','MM')
%
% ******************** Read Me - Very important notes ********************
% - This function will not work properly if the attenuation does not have
% enough inportant digits. So if you ask your timeseries to be smoothed
% with ATNincrement equal to 0.01 this means the attenuation input must
% have 3 decimal digits accuracy. This is very important for AE51 
% aethalometer model, which requires ATNincrement equal to 0.01 but the
% output attenuation is 2 digit accuracy and the does not work. In this
% case the user MUST calculate attenuation based on measurment and reference
% signals also provided in the output. Check Pikridas et al., 2019 AMT to
% learn how to do that.
%
% - Timeseries must be homogeneous. By homogeneous it is meant timeseries
% with an even step throughout. As an example STAP output is not
% homogeneous because even though it is evenly spaced, it contains gaps
% every 3-4 measurements when 1sec resolution is sought. The user must fill
% the gaps, eg by linear interpolation. 
%
% - When you apply smoothing the aim is to produce a realistic output.
% However when the sampling air mass concentration changes rapidly,
% smoothing may alter the result so that it no longers resembles the actual
% conditions. An example is to use a miniature absorption monitor to
% monitor the vertical gradient of the atmosphere. If you are inside an
% urban area starting from high concentration inside the mixing layer
% followed by a relatively clean layer above, by smoothing you will change
% the height of the transition from one layer to the other. The bias magnitude 
% is a function of the concentration difference between the two layers. 
% Using weights cures the problem.
%
% - Always check your output with raw data or with different methods, eg by 
% applying weights or not, using different attenuation increments, removing
% outliers, etc
%
% ************************Good Practices**********************************
% - Assuming you have a multiwavelength instrument you want to apply the same
% smoothing to all wavelengths. the best way is to do so iteratively using
% the same attenuation input but changing the response you want to smooth.
% The same approach can be applied if you want to smooth the same way an
% external variable for cross-checking.
%
% Test with many  ATN increments to find the best for the concentrations
% and instrument you are using.
% 
% Do not be afraid to combine the output from different methods, eg by
% using weights or not. This will allow you to get the best of this
% function for every setting possible.
%
% Cite the original work that this function was intended for if you used
% it. That is Pikridas et al., 2019, AMT
% **************** Known Bugs ********************************************
% When you apply weights the start and end of the timeseries may appear very noisy.
% This relates to the precision of the instrument used. Replace these noisy
% points with the non-weighed output.
%
% Michael Pikridas - The Cyprus Institute 

%% Setting default values. They are changed below based on user preferences
wl=NaN; % Obsolete input. Now used only to avoid errors
method='moving'; %which method is to be used
delATN=0.05; %which attenuation increment will be applied
flag=0; %default is not to apply weights
%% User Preferences
for i=1:length(varargin)
    
%     if strcmp(varargin{i},'wavelength')==1 % Setting user defined wavelength(s)
%         wl=varargin{i+1};
%     end
    
    if strcmp(varargin{i},'method')==1 % Setting user defined averaging method
        method=varargin{i+1};
    end
    
    if strcmp(varargin{i},'ATNincrement')==1 % Setting user defined Attenuation increment
        delATN=varargin{i+1};
    end
    
    if strcmp(varargin{i},'Weights')==1 % Restricting unequal number of forward and backward data points
        flag=varargin{i+1};
    end
    
end

%% Error Handling
for i=1:length(size(res)) %do the input sizes match
    if size(res,i)~=size(ATN,i)
        error('Size mismatch between inputs')
    end
    if i==1 && length(RealTime)~=size(res,1)
        error('Time vector length must match number of rows in the batn matrix')
    end
end

if numel(delATN)>1, error('Attenuation increment must be a single number'), end
if numel(wl)~=size(res,2), error('Either no wavelengths are provided or number of walengths given do not match number of response data columns'), end
if isvector(wl)==0, error('Wavelength must be given in vector form'), end

if strcmp(method,'moving')==0 && strcmp(method,'lowess')==0  && strcmp(method,'sgolay')==0 ...
        && strcmp(method,'average')==0 && strcmp(method,'originalaverage')==0
    error('Cannot identify the given method. Try ''moving'', ''lowess'', ''sgolay'', or ''average'' instead' )
end

if flag~=0 && flag~=1, error('Cannot determine whether to use or not weights. Use either 0 or 1 to specify'), end

%% Preparing the input
% Locate when the sample spot is changed based on Attenuation
for i=1:numel(wl) %for each wavelength input
    temp=abs(ATN(2:end,i)-ATN(1:end-1,i));
    temp=find(temp(:)>15 | isnan(temp));
    if isempty(temp)==0 %if values are found
        pl_atn(:,i)=temp;
    else
        pl_atn=[]; %prevents error
    end
end
pl_atn=pl_atn(:);%linearize. All wavelengths should give the same results.

% Locate when the sample spot is changed based on Time
temp=abs(RealTime(2:end)-RealTime(1:end-1));
p=nanmedian(temp); % Gets the most frequent time resolution. This assumes that the measurements of each input correspond to a single time resolution
pl_time=find(temp(:)>3*p | isnan(temp));
pl=sort([pl_atn;pl_time]);

%removing duplicate values from the pl variable
count=numel(pl);
while count>1
    if pl(count)==pl(count-1), pl(count)=[]; end
    count=count-1;
end

if isempty(pl)==0 %if filter changes are found
    filtchange(1:length(pl)+1,1)=0; %create a vector of zeros
    filtchange(2:end,1)=pl; %filtchange has the position of the filter changes
    filtchange(end+1,1)=length(ATN)-1;
else %if NO filter changes are found, eg AE51 case
    filtchange(1,1)=0;
    filtchange(2,1)=length(ATN)-1;
end
filtchange=filtchange+1; % Adding 1 so to locate where each sample spot started

% Locating the actual positions in the response matrix to perform the averaging
% The smoothing will be done on the longest wavelength if 880 nm is not available
switch numel(wl)
    case 1
        avg_wl=1; %if only one wavelength is given
    otherwise
        if isempty(wl==880)==0 || isempty(wl==0.88)==0 %if the 880 nm channel is given
            avg_wl=find(wl==880);%the column position of the res matrix upon which I will do the smoothing.
            if isempty(avg_wl), avg_wl=find(wl==0.88); end %in case it is expressed in um
        else
            avg_wl=find(wl==max(wl)); %if 880 is not available take the max
        end
end

%% Deciding which matrix positions will be averaged based on the wavelength found above
n=ones(size(res,1),1); %create a series of ones that will denote with how many points each measurement will be smoothed
pos=nan(size(res,1),2); %the positions that will be averaged, preallocating for speed
res_smoothed=res; % the smoothed output of this function, duplicating and preallocating memory

for k=1:length(filtchange)-1 %for every filter change found
    for j=filtchange(k):filtchange(k+1);
        if j<filtchange(k+1) %works for all j except the last one
            for_ind=find(ATN(j:filtchange(k+1)-1,avg_wl)<=ATN(j,avg_wl)+delATN/2);
            bk_ind=find(ATN(filtchange(k):j,avg_wl)>ATN(j,avg_wl)-delATN/2); %finds position of ATN lower than the initial ATN
        elseif j==filtchange(k+1) %special case for the last measurement
            for_ind=1;
            bk_ind=find(ATN(filtchange(k):j,avg_wl)>ATN(j,avg_wl)-delATN/2); %finds position of ATN lower than the initial ATN
        end
        if numel(for_ind)+numel(bk_ind)>1  %if values are found
            pos(j,:)=[bk_ind(1)+filtchange(k)-1,j+for_ind(end)-1]; %the positions to smooth over
            n(j)=numel(bk_ind(1)+filtchange(k)-1:j+for_ind(end)-1);
            if flag==1 %if weighed averages are used instead
                nbk(j)=numel(bk_ind(1)+filtchange(k)-1:j-1); % number of points corresponding backward
                nfor(j)=numel(j:j+for_ind(end)-1); %number of points corresponding forward
            end
        end
    end
end


%% Smoothing the instrument response

if strcmp(method,'average')  %the simple average identical to Hagler et al., 2011
    for i=1:numel(wl)
        [res_smoothed(:,i),n(:,i) ] = AethSmoothing_ONA( RealTime,res(:,i),ATN(:,i),delATN );
    end
    pos=[];
elseif strcmp(method,'moving')  %the rolling average
    for j=1:numel(wl) %for every wavelength
        for i=1:numel(n) %for every data point
            if isnan(pos(i,1))==1 || isnan(pos(i,2))==1, continue, end %typically the last value is not smoothed but causes error
                conditioned= res(pos(i,1):pos(i,2),j);
 
            
            %% Non-Weighed Average
            if flag==0 %the default using no weighing method
                res_smoothed(i,j)=nanmean(conditioned);
                res_std(i,j)=nanstd(conditioned);
                %% Weighing Average Method
            elseif flag==1 %if weighing average is used
                if numel(conditioned)~=nbk(i)+nfor(i), error('Sizes do not match'), end % Test to ensure that everything runs as planned
                av_bk=nanmean(conditioned(1:nbk(i))); %the backward average alone
                av_for=nanmean(conditioned(nbk(i)+1:end)); %the forward average alone
                nbk(i)=nbk(i)-numel(find(isnan(conditioned(1:nbk(i))))); %subtracts any NaN's
                nfor(i)=nfor(i)-numel(find(isnan(conditioned(nbk(j)+1:end)))); %subtracts any NaN's
                res_smoothed(i,j)= (av_bk*nfor(i)+av_for*nbk(i))/(nbk(i)+ nfor(i));
                weights=[nfor(i)*ones(size(conditioned(1:nbk(i)))); nbk(i)*ones(size(conditioned(nbk(i)+1:end)))];
                weights(isnan(conditioned)==1)=[]; %removing NaN's
                conditioned(isnan(conditioned)==1)=[]; %removing NaN's
                try
                    res_std(i,j) = sqrt(var(conditioned,weights)); % the variance of the weighed mean. the square root yields std
                catch
                    res_std(i,j)=NaN;
                end
            end
        end
    end
elseif strcmp(method,'lowess')
    [res_smoothed, res_std]=smoothing_lowess(res,pos,method);
elseif strcmp(method,'sgolay')
    [res_smoothed,res_std]=smoothing_sgolay(res,pos);
end
%% Providing some statistics
for i=1:numel(wl)
    fprintf('-------------------Results for #%d ---------------------------------\n',i)
    fprintf('Original average: %5.2f+-%5.2f. Smoothed average %5.2f+-%5.2f \n',nanmean(res(:,i)),nanstd(res(:,i)),nanmean(res_smoothed(:,i)),nanstd(res_smoothed(:,i)))
    fprintf('Original data included %d negative values (%5.2f%%). Smoothed data include %d negative values (%5.2f%%)\n',...
        numel(find(res(res(:,i)<0,i))),100*numel(find(res(res(:,i)<0,i)))/numel(res(:,i)),numel(find(res(res_smoothed(:,1)<0,i))),100*numel(find(res(res_smoothed(:,1)<0,i)))/numel(res(:,i)))
end
end %main function end

%--------------------------------------------------------------------------------------------------------------------------
function [res_smooth,n ] = AethSmoothing_ONA( RealTime,res,ATN,delATN )
try
    BC_ONA=[RealTime,res,ATN]; % concatenating the input according to instructions by Hagler et al., 2011 supplementary
catch
    error('Size Mismatch') %error handling
end
if nargin==3,delATN=0.05; end %ATN default incremental value

%% find filter change points
for i=2:size(BC_ONA,1)-1
    temp(i,1)=abs(BC_ONA(i+1,3)-BC_ONA(i,3));
end
pl=find(temp(:)>30 | isnan(temp));
clear temp
if isempty(pl)==0 %if filter changes are found, eg AE51 case
    filtchange(1:length(pl)+1,1)=0; %create a vector of zeros
    filtchange(2:end,1)=pl; %filtchange has the position of the filter changes
    filtchange(end+1,1)=length(BC_ONA);
else %if NO filter changes are found, eg AE51 case
    filtchange(1,1)=0;
    filtchange(2,1)=length(BC_ONA);
end
clear i pl

%% calculate smoothed BC, the heart of the code
BC_ONA(:,4)=1; %create a series of ones that will denote how many points were smoothed
for k=1:length(filtchange)-1 %for every filter change found
    j=filtchange(k)+1;  %set to first point after filter change
    for i=filtchange(k)+1:filtchange(k+1)
        if j<filtchange(k+1)
            if i==j
                des_ind=find(BC_ONA(j+1:filtchange(k+1),3)<=BC_ONA(j,3)+delATN); %finds position of ATN lower than the initial ATN
                if isempty(des_ind)==0 %if values are found
                    BC_ONA(j:des_ind(end)+j,2)=nanmean(BC_ONA(j:des_ind(end)+j,2)); %calculated smoothed new BC
                    BC_ONA(j:des_ind(end)+j,4)=length(BC_ONA(j:des_ind(end)+j,2));%calculate averaging period
                    j=j+des_ind(end)+1;
                else
                    j=j+1;
                end
            end
        end
    end
end
clear i j des_ind ans max_ind delATN k filtchange
res_smooth=BC_ONA(:,2); % the smoothed BC
n=BC_ONA(:,4); %how many data points are there

end
%--------------------------------------------------------------------------------------------------------------------------
function [sm, sdev]=smoothing_lowess(res,pos,method)
sm=res; %duplicating and preallocating memory
for j=1:size(res,2)
    for i=1:size(res,1)
        if isnan(pos(i,1))==1 || isnan(pos(i,2))==1, continue, end %typically the last value is not smoothed but causes error
        p=numel(pos(i,1):pos(i,2));
        switch p
            case {0,1}  %do nothing
                continue
            case 2 %in this case only rolling average can be applied
                sm(i,j)=nanmean(res(pos(i,1):pos(i,2),j));
            otherwise
                if rem(p,2)==0 %even numbers
                    temp=smooth([res(pos(i,1),j);res(pos(i,1):pos(i,2),j)],p+1,method);
                    sm(i,j)=temp(p/2+1); %gets the middle value
                elseif rem(p,2)==0 %odd numbers
                    temp=smooth(res(pos(i,1):pos(i,2),j),p,method);
                    sm(i,j)=temp(ceil(p/2)); %gets the middle value
                    sdev(i,j)=sqrt(sum((conditioned-sm(i,j)).^2)/(p-1));
                end
        end
    end
end
end

%-----------------------------------------------------------------------------------------------------------------------
function [sm, sdev]=smoothing_sgolay(res,pos)
sm=res; %duplicating and preallocating memory
sdev=res;
for j=1:size(res,2)
    for i=1:size(res,1)
        if isnan(pos(i,1))==1 || isnan(pos(i,2))==1, continue, end %typically the last value is not smoothed but causes error
        p=numel(pos(i,1):pos(i,2));
        switch p
            case {0,1}  %do nothing
                continue
            case 2 %in this case only rolling average can be applied
                sm(i,j)=nanmean(res(pos(i,1):pos(i,2),j));
            otherwise
                    conditioned= res(pos(i,1):pos(i,2),j);
                temp=smooth(conditioned,p,'sgolay',1);
                sm(i,j)=temp(ceil(p/2)); %gets the middle value
                sdev(i,j)=sqrt(sum((conditioned-sm(i,j)).^2)/(p-1));
        end
    end
end
end
