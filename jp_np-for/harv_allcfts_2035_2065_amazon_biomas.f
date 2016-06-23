c23456789
      program calc_harv
c
c determines yield for selected countries and states (see code's end)
      character(len=12) biomes
      integer index, counter
            
      real sc(720,360,26),sc2(720,360,13)
      real pais(720,360),paism(720,360)
      real estd(720,360),estdm(720,360)
      real mBR, frac(720,360,14),mpais
      real sc_area(720,360)
      real biomas_br(720,360), biomas_aux(720,360)
c
      open (10,file='hadcm3_2035_2065_avepotyields_H2Omass.bin',
     &    status='old',
     &    form='unformatted',access='direct',recl=720*360*4)
      open (11,file='cow2006.bin',
     &    status='old',
     &    form='unformatted',access='direct',recl=720*360*4)
      open (12,file='0.5_landarea.bin',
     &    status='old',
     &    form='unformatted',access='direct',recl=720*360*4)
     
      open (13, file='mask_biomes.flt',status='old',
     &    form='unformatted', access='direct', recl=720*360*4)
     
      open(17, file="bi_hadcm3_2035_2065_avepotyields_H2Omass.txt",
     &  status="new", action="write")
      close(17)
c
      call read26 (10,sc)
      read (11,rec=1) paism
      read (11,rec=2) estdm
      read (12,rec=1) sc_area
      read (13,rec=1) biomas_aux
      close (10)
      close (11)
      close (12)
      close (13)
c
      do i=1,720
        do j=360,1,-1
        pais(i,j)=paism(i,(361-j))
        estd(i,j)=estdm(i,(361-j))
        biomas_br(i,j)=biomas_aux(i,(361-j))
        enddo
      enddo
c
ccc Not considering irrigated yields
c      do k=14,26	!compute the average yield in cells with irrigation
c        do i=1,720
c          do j=1,360
c      if((sc(i,j,k).gt.0.0).and.(sc(i,j,k-13).gt.0.0)) then !if irrigated and rainfed yields are > 0...
c	   sc2(i,j,k-13)=(sc(i,j,k)+sc(i,j,(k-13)))/2 !average yield between rainfed and irrigated
c      elseif((sc(i,j,k).gt.0.0).and.(sc(i,j,k-13).le.0.0)) then !if irrigated is > 0 but rainfed not...
c         sc2(i,j,k-13)=sc(i,j,k) !equal to irrigated yield
c      elseif((sc(i,j,k).le.0.0).and.(sc(i,j,k-13).gt.0.0)) then !if irrigated is not > 0
c         sc2(i,j,k-13)=sc(i,j,k-13) !rainfed yield
c      endif
c          enddo
c        enddo
c      enddo

      biomes = 'amcaceppptma'
      counter=0
      
      do index = 1,12
       if (mod(index,2) .ne. 0) then
      write(*,*) ''
      write(*,*) ''
      write(*,*) biomes(index:index+1)
      write(*,*) ''
      write(*,*) '          CFT     t/ha'
      
       open(17, file="bi_hadcm3_2035_2065_avepotyields_H2Omass.txt", 
     & status="old",form='formatted',position="append", action="write")
     
     

      write(*,*) ' CFT       t/ha'
      write(17,*) biomes(index:index+1)
      write(17,*) 'cft',' t/ha'
      do k=1,13	!all cfts
      n=0
      mBR=0
      mpais=0
         do i=1,720
         do j=1,360
c     biome calculations
      ! BIOMAS
c     0 Amazonia
c     1 Caatinga
c     2 Cerrado
c     3 Pampas
c     4 Pantanal
c     5 Mata Atlantica
      if ((biomas_br(i,j).eq.counter) .and. (sc(i,j,k).gt.0)) then !for biomes
      
c      if((pais(i,j).eq.191).and.(sc(i,j,k).gt.0)) then
c      if(((estd(i,j).eq.197).or.(estd(i,j).eq.199).or.     !for legal Amazon only
c     & (estd(i,j).eq.200).or.(estd(i,j).eq.209).or.
c     & (estd(i,j).eq.210).or.(estd(i,j).eq.213).or.
c     & (estd(i,j).eq.219).or.(estd(i,j).eq.220).or.
c     & (estd(i,j).eq.224)).and.(sc(i,j,k).gt.0)) then
         mBR=mBR+(sc(i,j,k)*(sc_area(i,j)/13)) !Fresh matter yields
         n=n+(sc_area(i,j)/13)
      endif
         enddo
         enddo
      
      if(n .ne. 0) then
      mpais=(mBR/n)
      else mpais = 0 
      endif
            
      write(*,*) k, mpais
      write(17,*) k, mpais
      enddo
      close(17)    
      counter = counter+1
      endif
      enddo   
c
      stop
      end

c=======================================================================

      subroutine read13 (nunit,var)
c auxiliar reading routine
      parameter(nx=720,ny=360)
      integer nunit
      real var(nx,ny,13)
      real aux(nx,ny)
      do k=1,13
        read(nunit,rec=k) aux
        do i=1,nx
          do j=1,ny
            var(i,j,k) = aux(i,j)
          enddo
        enddo
      enddo
      return
      end

c=======================================================================

      subroutine read26 (nunit,var)
c auxiliar reading routine
      parameter(nx=720,ny=360)
      integer nunit
      real var(nx,ny,26)
      real aux(nx,ny)
      do k=1,26
        read(nunit,rec=k) aux
        do i=1,nx
          do j=1,ny
            var(i,j,k) = aux(i,j)
          enddo
        enddo
      enddo
      return
      end

ccccccccccccccccccccccccccccccccccccccccccccccc
ccccc
cArgentina 5
cAustria 7
cBrazil 191
cBulgaria 19
cCanada 192
cChile 29
cChina 193
cColombia 30
cCroatia 35
cEgypt 43
cEthiopia 48
cFrance 54
cGermany 61
cGreece 63
cHungary 72
cIndia 194
cIndonesia 74
cIran 75
cItaly 79
cKenya 85
cMexico 106
cNepal 114
cNigeria 120
cNorth Korea 121
cPakistan 125
cPhilippines 130
cPoland 132
cRomania 137
cRussia 195
cSerbia 142
cSouth Africa 148
cSpain 151
cTanzania 163
cThailand 164
cTurkey 169
cUkraine 173
cUnited States of America 196
cVenezuela 179
cVietnam 180
cccccc
c
c	
c	Acre 197
c	Alagoas	198
c	Amapa 199
c	Amazonas 200
c	Bahia 201
c	Ceara 202
c	Distrito_Federal 203
c	Espirito_Santo 204
c	Goias 205
c	Litigated_Zone 206
c	Mato_Grosso_do_Sul 207
c	Minas_Gerais 208
c	Mato_Grosso 209
c	Maranhao 210
c	Paraiba	211
c	Parana 212
c	Para 213
c	Piaui 214
c	Pernambuco 215
c	Rio_de_Janeiro 216
c	Rio_Grande_do_Norte 217
c	Rio_Grande_do_Sul 218
c	Rondonia 219
c	Roraima	220
c	Santa_Catarina 221
c	Sao_Paulo 222
c	Sergipe	223
c	Tocantins 224


