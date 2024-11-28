import styles from './app-header.module.css';
import { Home2, User } from 'iconic-react';
import { NavLink } from 'react-router-dom';
import { TAppHeaderUIProps } from './type';
import { FC } from 'react';
import photo from './photo.png';

type TNavLinkRender = {
  isActive: boolean;
};

export const AppHeaderUI: FC<TAppHeaderUIProps> = ({ userName }) => {
  const setActive = ({ isActive }: TNavLinkRender) =>
    `${styles.link} ${isActive ? styles.link_active : ''}`;

  return (
    <header className={styles.header}>
      <nav className={`${styles.menu} p-4`}>
        <div className={styles.menu_part_left}>
          <>
            <NavLink to='/' className={setActive}>
              <button className={styles.header_button}>
                <Home2 size='48' color='currentColor' variant='Bulk' />
                Главная
              </button>
            </NavLink>
          </>
        </div>
        <NavLink to='/' className={setActive}>
          <button className={styles.logo}>
            Happiness
            <img src={photo} />
            is near...
          </button>
        </NavLink>
        <div className={styles.link_position_last}>
          <NavLink to={userName ? 'profile' : 'login'} className={setActive}>
            <button className={styles.header_button}>
              <User size='48' color='currentColor' variant='Bulk' />
              {userName || 'Личный кабинет'}
            </button>
          </NavLink>
        </div>
      </nav>
    </header>
  );
};
